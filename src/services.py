import subprocess, time

class ServiceManager:
    
    stopped_services = []
    
    def disable(self, keep_alive=[]):
        
        active = subprocess.check_output(
            "service --status-all | grep + | grep -oe \"[a-zA-Z\\\\-]*\"",
            shell=True
        ).decode('ascii').split()

        # string of services to kill
        self.stopped_services = " ".join(list(filter(lambda x: x not in keep_alive, active)))

        for i in range(10,1,-1):
            print(f"Disabling services in {i} seconds")
            time.sleep(1)
        print("Disabling services now!")
        
        # stop unneeded services
        subprocess.run("sudo wifi off", shell=True)
        stop_ret = subprocess.run("sudo systemctl stop " + self.stopped_services, shell=True)
        
    def enable(self):
        start_ret = subprocess.run("sudo systemctl start " + self.stopped_services, shell=True)
        time.sleep(10)
        subprocess.run("sudo wifi on", shell=True)

        print("All services back online!")
