import pickle
import matplotlib.pyplot as plt
import seaborn as sns

with open("benchmark.p", 'rb') as f:
  benchmark = pickle.load(f)

times = []
accuracies = []

for class_name in benchmark:
  for single_bench in benchmark[class_name]:
    times.append(round(single_bench["time"], 4))
    accuracies.append(single_bench["accuracy"])

avg_time = sum(times) / len(times)
max_time = max(times)
min_time = min(times)

avg_acc = sum(accuracies) / len(accuracies)
max_acc = max(accuracies)
min_acc = min(accuracies)

print(avg_time, max_time, min_time)
print(avg_acc, max_acc, min_acc)

sns.displot(times)
plt.savefig("time_graph.png")

sns.displot(accuracies)
plt.savefig("accuracies_graph.png")