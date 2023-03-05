from bridge import Executor


if __name__ == "__main__":
    exe = Executor("contract.json")
    exe.enforce()
