import rrdtool # apt install python-rrdtool
import sys
import os

from sensors import SENSORS, RRD_DEFS  # Sensors config file


def main():
    for rrd, rrdparms in RRD_DEFS.iteritems():
        try:
            if not os.path.isfile(rrdparms['file']+".rrd"):
                print("RRD file %s missing, skipping" % rrdparms['file'])
                continue

            #print("creating: " + rrdparms['file']+".png")
            rrd_params_1 = list()
            rrd_params_2 = list()

            for sensor, params in SENSORS.iteritems():
                if params[0] == rrd:
                    # TODO min:max
                    rrd_params_1.append("DEF:"+params[3]+"="+rrdparms['file']+".rrd:"+ params[3] + ":AVERAGE")
                    rrd_params_2.append("LINE2:"+params[3]+"#"+params[2]+":"+params[3])

            # Create graphs
            rrd_params = rrd_params_1 + rrd_params_2 
            # 24h graph
            ret = rrdtool.graph(rrdparms['file']+"-24h.png", "--start", "-1d",
                "--vertical-label="+rrdparms['vertical-label'],
                "--width","1024", "--height","800",
                *rrd_params)
            # week graph
            ret = rrdtool.graph(rrdparms['file']+"-7d.png", "--start", "-7d",
                "--vertical-label="+rrdparms['vertical-label'],
                "--width","1024", "--height","800",
                *rrd_params)
            # month graph
            ret = rrdtool.graph(rrdparms['file']+"-30d.png", "--start", "-30d",
                "--vertical-label="+rrdparms['vertical-label'],
                "--width","1024", "--height","800",
                *rrd_params)

        except rrdtool.error as e:
            print("ERROR rrdtool: " + e.message)
        except Exception as e:
            print(sys.exc_info()[0])


if __name__ == "__main__":
    main()
