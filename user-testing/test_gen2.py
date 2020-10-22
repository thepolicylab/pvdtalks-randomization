
for n in [50, 500, 5000]:
    with open(f'ids_n_{n}.csv', 'wt') as outfile:
        outfile.write('\n'.join(map(str, np.random.choice(1_000_000, size=n))))
