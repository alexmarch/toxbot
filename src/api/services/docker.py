from docker import from_env, errors
from os import path

class Docker:
    def __init__(self, image_name):
        self.docker = from_env()
        self.image_name = image_name

    def is_image_exist(self):
        try:
            return self.docker.images.get(self.image_name)
        except errors.ImageNotFound:
            return False

    def build(self):
        dockerfile_path = path.normpath(path.join(path.dirname(__file__), '../../../'))
        try:
            (img, log) = self.docker.images.build(path = dockerfile_path, tag = self.image_name, rm=True)
            print("Docker image %s was created." % self.image_name)
            # self.docker.containers.run(tag)
        except errors.BuildError as err:
            print("Error", err)

    def getC(self, cid):
        return self.docker.containers.get(cid)

    def run(self, env, volumes):
        return self.docker.containers.run(image=self.image_name, environment=env, volumes=volumes, detach=True)