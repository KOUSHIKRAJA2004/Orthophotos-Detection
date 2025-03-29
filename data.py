from roboflow import Roboflow
rf = Roboflow(api_key="99RSk2Orrx1CvVrSdSbz")
project = rf.workspace("koushik-13i1h").project("orthophotos-wbptv")
version = project.version(4)
dataset = version.download("yolov8")