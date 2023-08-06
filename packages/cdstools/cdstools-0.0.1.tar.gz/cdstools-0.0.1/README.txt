This package offers users simple tools designed for Credit Default Swap (CDS) data. 
Included in this package is a hazard rate bootstrapping function which 
implements the JP Morgan model for determining hazard rate curves. To be Included
in future releases will be a pricing function that detemines a CDS's spread based
on the yield curve and default probabilities, and a function that prices Credit
Default Swaptions (options on CDSs).

Bootstrapping Function:
This function implements the so-called JP Morgan model. This model makes the 
assumptions that the interest rate process is independent of the default process
and that default leg pays at the end of each accrual period. Typically, regular
fee payments occur at the end of each period. To that end, this model assumes
that defaults occur midway buring each payment period. And finally, this model
assumes that the hazard rate is piecewise constant on the intervals that correspond
to the maturities of the CDS contracts.