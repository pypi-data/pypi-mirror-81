import numpy 
import matplotlib.pyplot as pyplot

# try:
#     '''
#     pip install pynufft
#     '''
#     from pynufft.pynufft import pynufft
# except:
#     print('warning: pynufft  not found in system library')
#     print('Try to import the local pynufft now')
#     import sys
#     sys.path.append('../pynufft')
#     from pynufft import pynufft
    

def example_1D():

    om = numpy.random.randn(1512,1)
    # print(om)
    # print(om.shape)
    # pyplot.hist(om)
    # pyplot.show()
    
    Nd = (256,) # time grid, tuple
    Kd = (512,) # frequency grid, tuple
    Jd = (7,) # interpolator 
    from pynufft import NUFFT_cpu, NUFFT_hsa
    NufftObj = NUFFT_cpu()
    
    
    NufftObj.plan(om, Nd, Kd, Jd)
    
    
    time_data = numpy.zeros(256, )
    time_data[64:192] = 1.0
    pyplot.plot(time_data)
    pyplot.ylim(-1,2)
    pyplot.show()
    
    
    nufft_freq_data =NufftObj.forward(time_data)
    
    restore_time = NufftObj.solve(nufft_freq_data,'cg', maxiter=30)
    
    restore_time2 = NufftObj.solve(nufft_freq_data,'L1TVOLS', maxiter=30,rho=1)
    
    im1,=pyplot.plot(numpy.abs(time_data),'r',label='original signal')
 
#     im2,=pyplot.plot(numpy.abs(restore_time1),'b:',label='L1TVLAD')
    im3,=pyplot.plot(numpy.abs(restore_time2),'k--',label='L1TVOLS')
    im4,=pyplot.plot(numpy.abs(restore_time),'r:',label='conjugate_gradient_method')
    pyplot.legend([im1,  im3,im4])
    
    
    pyplot.show()

if __name__ == '__main__':
    example_1D()
