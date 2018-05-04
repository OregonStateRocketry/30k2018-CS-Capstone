mydata=read.csv(file=file.choose())
boxplot.stats(mydata$Temp)$out
plot(Temp~Time, mydata)
lfit = lm(mydata$Temp~mydata$Time)
abline(lfit, col="red")
residual = resid(lfit)
boxplot.stats(residual)$out