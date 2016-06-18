import pycuda.autoinit
 
import pycuda.driver as cuda
 
device = cuda.Device(0)
 
import pprint
 
pp = pprint.PrettyPrinter(depth=10)
 
pp.pprint(device.get_attributes())
