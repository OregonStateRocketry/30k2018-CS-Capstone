mydata=read.csv(file=file.choose())
boxplot.stats(mydata$Accel)$out
plot(Accel~Time, mydata)
lfit = lm(mydata$Accel~mydata$Time)
abline(lfit, col="red")
residual = resid(lfit)
boxplot.stats(residual)$out