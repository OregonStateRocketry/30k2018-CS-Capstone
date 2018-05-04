mydata=read.csv(file=file.choose())
boxplot.stats(mydata$Alt)$out
plot(Alt~Time, mydata)
lfit = lm(mydata$Alt~mydata$Time)
abline(lfit, col="red")
residual = resid(lfit)
boxplot.stats(residual)$out