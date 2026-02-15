from agent import run_agent

if __name__ == "__main__":
    q = input("Ask: ")
    ans = run_agent(q)
    print("\nFINAL:", ans)
