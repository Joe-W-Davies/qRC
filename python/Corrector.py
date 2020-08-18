import numpy as np

class Corrector:
   
   # store regressor predictions and Y target
   def __init__(self,mcclf,dataclf,X,Y,diz=False):
      self.diz=diz #Flag for distribution with discrete 0, i.e. Isolation
      #store Y prediction for data and mc chunk X
      self.mcqtls   = np.array([clf.predict(X) for clf in mcclf])
      self.dataqtls = np.array([clf.predict(X) for clf in dataclf])

      #NOTE: contructor is returning [[pred_bdt_q1], [pred_bdt_q2], ...],
      #      this is a (N,d) array where N is #evts and d is #quantiles
      #      so for each individual event, each  BDT is returning
      #      a prediction of the CDF at some quantile for the target variable, given the X features for that event. 
      #      We are essentially populating 21 points on the CDF for Data and MC for a single event
      #      so we can map the true y_value in MC to that observed in the data CDF
      #      (after interpolating between the 21 quantiles to get the full distribution)

      self.Y = Y

      print(''' q's of CDF predicted in MC:   {}'''.format(self.mcqtls))
      print(' shape of CDF predicted in MC:   {}'.format(self.mcqtls.shape))
      print(''' q's of CDF predicted in Data: {}'''.format(self.dataqtls))
      print(' shape of CDF predicted in Data: {}'.format(self.dataqtls.shape))
      
   def correctEvent(self,iev):
      ''' 
      Function that applies the correction to MC.

      For a single event, get the 21 predicted quantiles of the CDF for both data and MC.
      Gets the lower and upper quantiles that bound the predicted Y value, for the event (window around Y).
      Interpolate between this window to get the intermediate CDF value between the two quantiles, and the corresponding Y value here.
      Do the same in Data, then map Y_mc to Y_data by reading the corresponding CDF(y_i|X_i)_mc and mapping this to same point in data,
      and then reading of the Y_data value as the correction
  
      '''
      
      mcqtls = self.mcqtls[:,iev]
      dataqtls = self.dataqtls[:,iev]
      Y = self.Y[iev]
      
      if self.diz and Y == 0.:
         return 0.

      #quantile counter      
      qmc =0
      
      #count up to the quantile that is the closest to the predicted Y-value i.e. the bounding lower quantile of the CDF
      while qmc < len(mcqtls): # while + if, to avoid bumping the range
         if mcqtls[qmc] < Y:
            qmc+=1
         else:
            break

      # all shower shapes have a lower bound at 0, so if Y is in first quantile, lower bound is zero (if correcting SS's)
      # upper bound is just the value of the Y at the 1st (0th list index) quantile
      if qmc == 0:
         qmc_low,qdata_low   = 0,0                              
         qmc_high,qdata_high = mcqtls[qmc],dataqtls[qmc]
      # otherwise, get the bounding CDF quantiles that the Y value sits in from indexer computed above
      elif qmc < len(mcqtls):
         qmc_low,qdata_low   = mcqtls[qmc-1],dataqtls[qmc-1]
         qmc_high,qdata_high = mcqtls[qmc],dataqtls[qmc]
      # if inside the top quantile, we have no "higher" quantile, so generate atrifically as: (Y value at max quantile * 1.2) 
      # use this in the interpolation
      else:
         qmc_low,qdata_low   = mcqtls[qmc-1],dataqtls[qmc-1]
         qmc_high,qdata_high = mcqtls[len(mcqtls)-1]*1.2,dataqtls[len(dataqtls)-1]*1.2
                                                                       
      #do interpolation between quantiles (Y values) for neighbouring quantile points and read Y in data correponding (in the CDF) to Y in MC
      #assumes straight line between points (Y_low-mc, Y_low-data) and (Y_high-mc, Y_high-data), which Y_pred (just labelled Y) lies on
      return (qdata_high-qdata_low)/(qmc_high-qmc_low) * (Y - qmc_low) + qdata_low

   def __call__(self):
      return np.array([ self.correctEvent(iev) for iev in xrange(self.Y.size) ]).ravel()

def applyCorrection(mcclf,dataclf,X,Y,diz=False):
   #instance is created and built-in method is called 
   return Corrector(mcclf,dataclf,X,Y,diz)()
