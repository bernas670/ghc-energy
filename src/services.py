import subprocess, time

class Services:
    
    stopped_services = []
    
    def disable(self, keep_alive=[]):
        
        active = subprocess.check_output(
            "service --status-all | grep + | grep -oe \"[a-zA-Z\\\\-]*\"",
            shell=True
        ).decode('ascii').split()

        # string of services to kill
        self.stopped_services = " ".join(list(filter(lambda x: x not in keep_alive, active)))

        for i in range(10,1,-1):
            print(f"Disabling services in {i} seconds\n")
            time.sleep(1)
        print("Disabling services now!")
        
        # stop unneeded services
        subprocess.call("sudo wifi off")
        stop_ret = subprocess.call("sudo systemctl stop " + self.stopped_services)
        
    def enable(self):
        start_ret = subprocess.call("sudo systemctl start " + self.stopped_services)
        time.sleep(10)
        subprocess.call("sudo wifi on")

        print("All services back online!")