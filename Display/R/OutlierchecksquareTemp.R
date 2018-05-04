mydata=read.csv(file=file.choose())
boxplot.stats(mydata$Temp)$out
plot(Temp~Time, mydata)
Time2 <- mydata$Time^2
lfit = lm(mydata$Temp~mydata$Time + Time2)
abline(lfit, col="red")
residual = resid(lfit)
boxplot.stats(residual)$out