import subprocess
import threading
import time

out = subprocess.run(["openai", "tools", "fine_tunes.prepare_data", "-f", "datasets/openai_datasets/bitcoin_chatbot_training_data.jsonl"], capture_output=True)
# out = out.decode("utf-8")
print(out)


# def some_function(a):
#     if a < 5:
#         print("sleeping 5 seconds")
#     time.sleep(5)
#     print(a)

# threads = []
# for i in range(10):
#     t = threading.Thread(target=some_function, args=(i,))
#     t.start()
#     threads.append(t)

# for t in threads:
#     t.join()

