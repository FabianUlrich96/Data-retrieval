import digitalocean
import time

class DigitalOceanAPI:

    @staticmethod
    def create_droplet(name):
        image = 'squid-template'
        token = "49fe5fdab11f17a3415ea04c7e3de420eed5f741f6a8a354e2a5b374b791c362"
        manager = digitalocean.Manager(token=token)
        snapshots = [m for m in manager.get_all_snapshots()
                     if m.name == image]
        image = snapshots[0].id if snapshots else image

        droplet = digitalocean.Droplet(token="49fe5fdab11f17a3415ea04c7e3de420eed5f741f6a8a354e2a5b374b791c362",
                                       name=name,
                                       region='fra1',  # Frankfurt 1
                                       image=image,  # Ubuntu with squid proxy
                                       size_slug='s-1vcpu-1gb',  # 1GB RAM, 1 vCPU
                                       backups=False)
        droplet.create()
        time.sleep(10)
        return droplet

    @staticmethod
    def check_status(droplet):
        actions = droplet.get_actions()
        for action in actions:
            action.load()
            # Once it shows "completed", droplet is up and running
            status = action.status
            return status
