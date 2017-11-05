import os.path
import sys
import rrdtool
from sensors import RRD_DEFS, SENSORS

# 24h with 2,5 min resolution
# 7d with 5 min resolution
# 1y with 10 min resolution
# 20y with 1h resolution

for rrd, rrdparms in RRD_DEFS.iteritems():
    try:
        if os.path.isfile(rrdparms['file']+".rrd"):
            print("RRD file %s exists, skipping" % rrdparms['file'])
            continue
        rrd_params = list()
        print("creating: " + rrdparms['file']+".rrd")
        for sensor, params in SENSORS.iteritems():
            if params[0] == rrd:
                # TODO min:max
                rrd_params.append("DS:" + params[3] + ":GAUGE:300:U:U")
        if rrd_params:
            rrd_params += ["RRA:AVERAGE:0.5:1:576",
                    "RRA:AVERAGE:0.5:2:2016",
                    "RRA:AVERAGE:0.5:4:52560",
                    "RRA:AVERAGE:0.5:24:175200",
                    "RRA:MAX:0.5:1:576",
                    "RRA:MAX:0.5:2:2016",
                    "RRA:MAX:0.5:4:52560",
                    "RRA:MAX:0.5:24:175200",
                    "RRA:MIN:0.5:1:576",
                    "RRA:MIN:0.5:2:2016",
                    "RRA:MIN:0.5:4:52560",
                    "RRA:MIN:0.5:24:175200"]
            print(rrd_params)
            ret = rrdtool.create(rrdparms['file']+".rrd", "--step", "300",
                    "--start", '0',
                    *rrd_params)
            if ret:
                print(rrdtool.error())
        else:
            print("Skipping " + rrdparms['file'] + ", no sensors defined")
    except rrdtool.error as e:
        print("ERROR rrdtool: " + e.message)
    except Exception as e:
        print("ERROR " + sys.exc_info()[0])
