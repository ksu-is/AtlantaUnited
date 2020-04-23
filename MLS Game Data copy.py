import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

##url = "https://raw.githubusercontent.com/jalapic/engsoccerdata/master/data-raw/mls.csv"
##c = pd.read_csv(url)
##c.to_csv('mls_goals_data.csv')

df = pd.read_csv('mls_goals_data_revised.csv', index_col='Season')
print(df.columns)
hGoals = []
vGoals = []
years = []
hWins = []
vWins = []
numTies = []
numTeamsByYear =[]

##Add "home win?" column for easier access in later calculations: options will be hwin, awin, tie
# conditions = [(df['hgoal'] > df['vgoal']) | (df['hgoalaet'] > df['vgoalaet']) | (df['hpen'] > df['vpen']),
#               (df['hgoal'] < df['vgoal']) | (df['hgoalaet'] < df['vgoalaet']) | (df['hpen'] < df['vpen']),
#               (df['hgoal'] == df['vgoal']) & (df['hgoalaet'].isnull())]
# choices = ['h', 'a', 't']
#
# df['hwins'] = np.select(conditions, choices, default=pd.np.NaN)

#count up total goals and wins (home and away) scored each year
for year in range(1996,2017):
    hGoals.append(df.loc[year, 'hgoal'].sum())
    vGoals.append(df.loc[year, 'vgoal'].sum())
    years.append(year)
    hvt = df.loc[year, 'hwins'].value_counts().tolist()
    hWins.append(hvt[0])
    vWins.append(hvt[1])
    if len(hvt) > 2:
        numTies.append(hvt[2])
    else:
        numTies.append(0)
    numTeamsByYear.append(len(df.loc[year,'home'].value_counts().tolist()))

goalDiff = []
winDiff = []
hGoalsPerTeams = []
vGoalsPerTeams = []
#Calculate goal differential and win differential for each year
for i in range(len(hGoals)):
    goalDiff.append(hGoals[i] - vGoals[i])
    winDiff.append(hWins[i] - vWins[i])
    hGoalsPerTeams.append(hGoals[i] / numTeamsByYear[i])
    vGoalsPerTeams.append(vGoals[i] / numTeamsByYear[i])

print("Home Goals: ", end='')
print(hGoals)
print("Vis Goals: ", end='')
print(vGoals)
print("Home Wins: ", end='')
print(hWins)
print("Vis Wins: ", end='')
print(vWins)
print("Ties by Year: ", end='')
print(numTies)
print("Number of Teams", end='')
print(numTeamsByYear)

## Create a model for the relationship between goals scored and games won
modelH = sm.OLS(hWins, hGoals).fit()
modelV = sm.OLS(vWins, vGoals).fit()
predictionsH = modelH.predict(hGoals)
predictionsV = modelV.predict(vWins)


fig1, ax = plt.subplots(nrows = 2, ncols = 3, figsize=(15, 9))

ax1 = plt.subplot(2,3,1)
ax1.set_title("Home v. Away Goals in MLS")
ax1.set_xlabel("Year")
ax1.set_ylabel("# of Goals")
ax1.set_xticks(range(np.min(years), np.max(years)+1, 2))
ax1.set_yticks(range(0, 700, 100))
ax1.plot(years, hGoals, color='blue', linestyle='solid')
ax1.plot(years, vGoals, color='red', linestyle='solid')
ax1.plot(years, goalDiff, color='purple', linestyle='solid')
ax1.set_ylim(ymin=0)
ax1.axhline(y=0, color='k')
ax1.legend(("Home", "Away", "Goal Differential"), loc=2)

ax2 = plt.subplot(2,3,2)
ax2.set_title("Home v. Away Wins in MLS")
ax2.set_xlabel("Year")
ax2.set_ylabel("# of Wins")
ax2.set_xticks(range(np.min(years), np.max(years)+1, 2))
ax2.set_yticks(range(0, 300, 50))
ax2.plot(years, hWins, color='blue', linestyle='solid')
ax2.plot(years, vWins, color='red', linestyle='solid')
ax2.plot(years, winDiff, color='purple', linestyle='solid')
ax2.plot(years, numTies, color='green', linestyle='solid')
ax2.set_ylim(ymin=0)
ax2.axhline(y=0, color='k')
ax2.legend(("Home", "Away", "Win Differential", "Ties"), loc=2)

ax3 = plt.subplot(2,3,3)
ax3.set_title("Average Home v. Away Goals Per Team in MLS")
ax3.set_xlabel("Year")
ax3.set_ylabel("# of Goals")
ax3.set_xticks(range(np.min(years), np.max(years)+1, 2))
ax3.set_yticks(range(0, 300, 5))
ax3.plot(years, hGoalsPerTeams, color='blue', linestyle='solid')
ax3.plot(years, vGoalsPerTeams, color='red', linestyle='solid')
ax3.set_ylim(ymin=0)
ax3.axhline(y=0, color='k')
ax3.legend(("Home", "Away"), loc=0)

ax4 = plt.subplot(2,3,4)
ax4.set_title("Average Wins v. Goals in MLS")
ax4.set_xlabel("# of Goals")
ax4.set_ylabel("# of Wins")
ax4.set_xticks(range(0, np.max(hGoals)+1, 30))
ax4.set_yticks(range(0, np.max(hWins), 10))
ax4.plot(hGoals, hWins, 'o', color='blue')
ax4.plot(vGoals, vWins,'o', color='red')
ax4.plot(hGoals, modelH.fittedvalues, 'b--', label='Home OLS')
ax4.plot(vGoals, modelV.fittedvalues, 'r--', label='Vis OLS')
ax4.set_ylim(ymin=0)
ax4.axhline(y=0, color='k')
ax4.text(360, 40, ("Home R^2 = {}%".format(np.trunc(100*modelH.rsquared))))
ax4.text(360, 20, ("Vis R^2 = {}%".format(np.trunc(100*modelV.rsquared))))
ax4.legend(("Home", "Away"), loc=0)

ax5 = plt.subplot(2,3,5)
ax5.set_title("Home v. Away Wins in MLS")
ax5.set_xlabel("Year")
ax5.set_ylabel("# of Wins")
ax5.set_xticks(range(np.min(years), np.max(years)+1, 2))
ax5.set_yticks(range(0, 300, 50))
ax5.plot(years, hWins, color='blue', linestyle='solid')
ax5.plot(years, vWins, color='red', linestyle='solid')
ax5.set_ylim(ymin=0)
ax5.axhline(y=0, color='k')
ax5.legend(("Home", "Away"), loc=2)
#but home and away goals aren't the whole story.  What about goals per # of teams?  More teams each year so see if goals per team increases
#relationship between goals and wins? regression for overall MLS and each team


plt.show()


