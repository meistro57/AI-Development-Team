from agents import list_default_agents

def verify_agents():
    all_ok = True
    for agent in list_default_agents():
        result = agent.perform_task('diagnostic')
        expected = f"{agent.name} executed task: diagnostic"
        if result != expected:
            print(f"❌ {agent.name} failed: got '{result}', expected '{expected}'")
            all_ok = False
        else:
            print(f"✅ {agent.name} functional")
    return all_ok

if __name__ == "__main__":
    if verify_agents():
        print("🎉 All agents are functional!")
    else:
        print("❌ Some agents failed diagnostics.")
