string = "Score: 6 Reason: This product contains multiple types of cheese, which are good sources of protein and calcium. However, the pasta has been enriched which means nutrients were added after processing. The added nutrients are typically vitamins and minerals, which is good for consumer health."
score = string.split()[1]
reason = string.split(': ')[2]
score = int(score)
print(score)
print(reason)
