.PHONY: test clean

test:
	pytest -q

clean:
	rm -f artifacts/*.jsonl artifacts/*.pcap artifacts/*.csv
