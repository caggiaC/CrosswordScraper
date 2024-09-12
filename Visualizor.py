import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd
import numpy as np


def do_twinx(frame):
    fig, ax = plt.subplots()
    axt = ax.twinx()

    x = frame.loc['letter']
    data1 = frame.loc['first']
    data2 = frame.loc['last']
    width = 0.2

    ax.set_xlabel("Letter")
    ax.set_ylabel("Appears As First Letter", color='blue')
    ax.set_ylim(0, 2500)
    data1.plot(kind='bar', color='blue', ax=ax, width=width, position=1)
    # ax.bar(x, data1, color='blue')

    axt.set_ylabel("Appears As Last Letter", color='red')
    axt.set_ylim(0, 2500)
    data2.plot(kind='bar', color='red', ax=axt, width=width, position=0)
    # axt.bar(x, data2, color='red')
    plt.show()


def do_phones(frame):
    fig, ax = plt.subplots(figsize=(10,6))
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    x = frame.index
    data = frame['count']

    data.plot(kind='bar', ax=ax, width=0.4)
    plt.show()


def do_words(frame):
    frame.set_index('word')
    frame = frame.sort_values('count', ascending=False)
    top_results = frame.head(20)
    data1 = top_results['count']
    data2 = top_results['length']
    x = top_results['word']

    fig, ax = plt.subplots()
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    # data1.plot(kind='bar', ax=ax, width=0.4)
    ax.bar(x, data1)
    plt.show()


def do_hist(frame):
    fig, ax = plt.subplots()

    x = frame['length']

    ax.set_xlabel("Word Length")
    ax.hist(x, bins=12, edgecolor='white')
    plt.show()


def length_freq(frame):
    frame = frame.sort_values('length', ascending=True)
    fig, ax = plt.subplots()
    x = frame['length']
    y = frame['count']

    ax.scatter(x, y)
    ax.set_xlabel('Word Length')
    ax.set_ylabel('Word Frequency')
    plt.show()


def main():
    letters_frame = pd.read_json("letters.json")
    phone_series = pd.read_json("phones.json", typ='series')
    phone_frame = phone_series.to_frame('count')
    words_frame = pd.read_json("words.json")
    do_twinx(letters_frame)
    do_phones(phone_frame)
    do_words(words_frame)
    do_hist(words_frame)
    length_freq(words_frame)


if __name__ == "__main__":
    main()
