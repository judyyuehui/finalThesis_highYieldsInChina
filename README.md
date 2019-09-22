# Final Thesis High Yields Risk Factor Cross Sectional Analysis In Chinese Market
Judy Yue's final thesis and codes at THU

## Abstract of the research:   
  In the context of financial regulation and leverage control, the existence of China's high- yield bond market has become possible. This paper focuses on the premium effect of the main risk factors in the domestic high-yield market. I use two high-yield bond definition and conduct separate research. I have found that high-yield markets have significant high- yield and high-risk characteristics and are more susceptible to economic shocks. Using univariate and bivariate ranking of variate risk factors, we found that there is a significant correlation between downside risk and lagged return, while liquidity risk is significantly less predictive. In later **cross-sectional regression**, we control for the remaining factors of bond duration, price momentum, volatility as well as the common used macro factors(***both from stock markets and bond markets***). The results show that the premium effect of the downside risk is significant at the 1% level, and the premium effect of the liquidity risk is significant at the 5% level. In the **Fama-Macbeth regression***, the downside risk factor remains significant, while the liquidity risk factor fluctuates significantly. More specifically, after 2016 August, the risk premium effect of the high-yield market is more significant, the high-yield bond rating is significantly negatively correlated with lagged returns, which indicating the chaos in domestic bond ratings system and the high risk aversion of investors. 
   
   
## Description of Each File:   
 
1. ReadMe  
2. 毕业论文.pdf   
   The first draft of the paper, still working on the second version(explore more on the comparasion and the robust of the downside risk factor)  
3. Codes:   
   ***a. data_process***:   
      i. data_process.py:   
      convert the raw data(downloaded from RESSET & Wind databases) to the monthly data  
      calculated the primary factors(including the major 4 factors)  
      ii. additionalDataProcess.py  
      insert more factors, calculated in other methods  
    ***b. statistics***:   
      i. Statistical Analysis_Basics&Sortings.ipynb  
          do the basic data analysis: null value analysis, factor statistics analysis, normality tests  
          conduct factor sortings  (return deciles divided by the rank of factor value)  
          
      ii. CalulateMacroBeta.ipynb  
          use the factor data to calculate the macro beta(regression and get the \alpha), calculation method is similar to the previous study in factor analysis  
          
      iii. sort functions.py  
          the sorting functions used in Statistical Analysis_Basics&Sortings.ipynb  
          
      iv. regression.py  
          conduct linear regressions and ***Fama-Macbeth regressions*** on various factors.   
       
      v. pca_analysis  
          base on the factors, conduct pca analysis using two packages(make sure that the result is correct)  
      
          
