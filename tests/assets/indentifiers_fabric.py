import os, random, glob
import pyessv, json
from pyessv import IDENTIFIER_TYPE_FILENAME, IDENTIFIER_TYPE_DATASET, IDENTIFIER_TYPE_DIRECTORY

# need acces to /bdd to parse directory and filename with pyessv and create list identifiers files
pyessv.load("compil")
auth = pyessv.COMPIL
mountdir = "/home/ltroussellier/Bureau/CicladMount" # sshfs spirit:.  Bureau/CicladMount -o follow_symlinks

def getnextrandompath(path):
    alls = glob.glob(os.path.join(path, "*"))
    #print(path)
    for p in alls:
        #print(p)
        if p.split("/")[-1] == "latest":
            alls.remove(p)
        if p.split("/")[-2] == "files":
            alls.remove(p)
            alls.append(p.replace("files/d", "v"))  ## pour CORDEX-Adjust
        if p.split("/")[-1] == "files":
            alls.remove(p)

    if len(alls) == 0:
        return path
    return getnextrandompath(random.choice(alls))


def get_random_sample(project):
    completepath = getnextrandompath(mountdir+"/bdd/" + project)
    filename = completepath.split("/")[-1]
    # print(filename)
    if filename[-2:] != "nc":  # il n'y a pas de file à la fin de l'arborescence .. on relance la fonction
        return -1, -1, -1
    dirname = "/".join(completepath.split("/")[:-1]).replace("/bdd/", "").replace(mountdir, "")

    if project == "CMIP5" and dirname.find("output"):
        dirname = dirname.replace("output", "output1")

    return filename, dirname, get_dataset_identifier(project, filename, dirname)


def get_dataset_identifier(project, fn, dire):
    try:
        t_dir = pyessv.parse_identifer(auth[project], pyessv.IDENTIFIER_TYPE_DIRECTORY, dire)
        #print(t_dir)
        t_fn = pyessv.parse_identifer(auth[project], pyessv.IDENTIFIER_TYPE_FILENAME, fn)
        #print(project)
        if (project == "CORDEX" or project == "CORDEX-Adjust"):
            m_model = ""
            m_inst = ""
            for k in t_dir:

                if k.collection == auth[project]["rcm_model"]:
                    m_model = k.name
                if k.collection == auth[project]["institution"]:
                    m_inst = k.name

                if m_model != "" and m_inst != "":
                    break

            m_name = m_model.replace(m_inst + "-", "")
            t_dir.add(auth[project]["rcm_name"][m_name])

        #print(t_fn)
        a = pyessv.build_identifier(auth[project], pyessv.IDENTIFIER_TYPE_DATASET, t_dir | t_fn)
        print(a)
        print("")
        return a
    except ValueError as e:
        print(e)
        print("PB :", dire, fn)
    except AttributeError:
        print("GROS PB : ,", dire, fn)


def get_list_random_sample(project, nb):
    filenames = []
    dirnames = []
    datasetnames = []
    for i in range(nb):
        f, d, da = get_random_sample(project)
        if f != -1 and da != None:
            filenames.append(f)
            dirnames.append(d)
            datasetnames.append(da)
    return filenames, dirnames, datasetnames


def print_examples(project, nb):
    print("COUCOUCOUCOU", auth[project])
    fs, ds, das = get_list_random_sample(project, nb)
    print("FILENAME EXAMPLES FOR", project)
    print(fs)
    print("DIRNAME EXAMPLES FOR", project)
    print(ds)
    print("DATASETS EXAMPLES FOR", project)
    print(das)


def create_all_json_for_project(project, nb):
    fs, ds, das = get_list_random_sample(project, nb)

    scope = auth[project]

    create_json(scope, fs, IDENTIFIER_TYPE_FILENAME)
    create_json(scope, ds, IDENTIFIER_TYPE_DIRECTORY)
    create_json(scope, das, IDENTIFIER_TYPE_DATASET)


testmapid = {IDENTIFIER_TYPE_FILENAME: "filename", IDENTIFIER_TYPE_DATASET: "dataset",
             IDENTIFIER_TYPE_DIRECTORY: "directory"}
"""    		
mapid = {"filename": IDENTIFIER_TYPE_FILENAME, "dataset": IDENTIFIER_TYPE_DATASET,
             "directory": IDENTIFIER_TYPE_DIRECTORY}
"""


def create_json(scope, identifiers, identifier_type):
    mdic = {"scope": scope.namespace}
    mdic["identifiers"] = identifiers
    # identifierstr=[k for k, v in mapid.items() if v == identifier_type][0]
    identifierstr = testmapid[identifier_type]
    json_name = identifierstr + "_" + scope.namespace.replace(":", "_").split("_")[-1] + ".json"
    with open("identifiers/" + json_name, "w") as outfile:
        print("WRITING : ", "identifiers/" + json_name)
        json.dump(mdic, outfile, indent=4)

def create_all(nb):
    create_all_json_for_project("CMIP6", nb)
    create_all_json_for_project("CMIP5", nb)
    create_all_json_for_project("CORDEX", nb)
    create_all_json_for_project("CORDEX-Adjust", nb)
    create_all_json_for_project("TAMIP", nb)
    create_all_json_for_project("EUCLIPSE", nb)
    create_all_json_for_project("PMIP3", nb)
    # create_all_json_for_project("input4MIPs", nb) NOT in COMPIL scope
    # create_all_json_for_project("obs4MIPS", nb)   NOT in COMPIL scope

create_all(100)
