AGENTS_MD_CONTENT = """
# Agent Configuration
## System Status
Current operational status: operational
Last updated: 2023-01-01 10:00:00
---
# Agent Tasks
- Monitor system health
- If system status is 'operational', proceed with task A.
- If system status is 'maintenance', defer task A.
"""

def parse_static_agent_info(content: str) -> dict:
    """
    Simulates parsing information from a static AGENTS.md file.
    In a real scenario, this might involve more complex parsing.
    """
    info = {}
    for line in content.split('\n'):
        if 'Current operational status:' in line:
            info['static_status'] = line.split(':')[-1].strip()
        if 'Last updated:' in line:
            info['static_last_updated'] = line.split(':')[-1].strip()
    return info

# --- Simulated Real-time System Status Source ---
# This function simulates fetching the actual, current status of a system.
# This data is dynamic and reflects the true state.
_current_system_status = "operational"

def get_realtime_system_status() -> str:
    """
    Simulates fetching the current, real-time status of the system.
    This would typically be an API call or database query.
    """
    global _current_system_status
    return _current_system_status

def update_realtime_system_status(new_status: str):
    """Helper to simulate a change in the real-time system status."""
    global _current_system_status
    _current_system_status = new_status
    print(f"\n--- Real-time system status updated to: '{new_status}' ---")

# --- Agent Logic ---

def agent_task_based_on_static_info(agent_name: str, static_info: dict):
    """
    An agent making decisions *solely* based on potentially stale static information.
    This demonstrates the problem described in the article.
    """
    status = static_info.get('static_status', 'unknown')
    print(f"\n[{agent_name} - Static Info Agent]")
    print(f"  Reading static AGENTS.md (last updated: {static_info.get('static_last_updated')})")
    print(f"  Static status perceived: '{status}'")

    # --- ARTICLE CONCEPT: Agent blindly trusts static info ---
    if status == 'operational':
        print(f"  Decision: System is operational. Proceeding with Task A.")
        # In a real scenario, this could lead to errors if the system is actually in maintenance.
    elif status == 'maintenance':
        print(f"  Decision: System is in maintenance. Deferring Task A.")
    else:
        print(f"  Decision: Unknown status. Taking cautious action.")

def agent_task_with_dynamic_validation(agent_name: str, static_info: dict):
    """
    An agent that validates static information with a dynamic, real-time source.
    This demonstrates a solution to the problem.
    """
    static_status = static_info.get('static_status', 'unknown')
    realtime_status = get_realtime_system_status() # Fetch real-time data

    print(f"\n[{agent_name} - Dynamic Validation Agent]")
    print(f"  Reading static AGENTS.md (last updated: {static_info.get('static_last_updated')})")
    print(f"  Static status perceived: '{static_status}'")
    print(f"  Fetching real-time status: '{realtime_status}'")

    # --- ARTICLE CONCEPT: Agent validates static info with dynamic data ---
    if static_status != realtime_status:
        print(f"  WARNING: Static AGENTS.md status ('{static_status}') conflicts with real-time status ('{realtime_status}').")
        print(f"  Prioritizing real-time status for decision making.")
        status_for_decision = realtime_status
    else:
        print(f"  Static AGENTS.md status matches real-time status. Proceeding with confidence.")
        status_for_decision = static_status

    if status_for_decision == 'operational':
        print(f"  Decision: System is operational. Proceeding with Task A.")
    elif status_for_decision == 'maintenance':
        print(f"  Decision: System is in maintenance. Deferring Task A.")
    else:
        print(f"  Decision: Unknown status. Taking cautious action.")


# --- Simulation Run ---
if __name__ == "__main__":
    print("--- Simulation Start ---")

    # 1. Agent starts, reads AGENTS.md, and real-time status matches.
    print("\nScenario 1: Initial state - AGENTS.md is up-to-date with real-time status.")
    static_agent_info = parse_static_agent_info(AGENTS_MD_CONTENT)
    print(f"Initial AGENTS.md static info: {static_agent_info}")
    print(f"Initial real-time status: '{get_realtime_system_status()}'")

    # Both agents should make the correct decision
    agent_task_based_on_static_info("Agent Alpha", static_agent_info)
    agent_task_with_dynamic_validation("Agent Beta", static_agent_info)

    # 2. Real-time system status changes, but AGENTS.md is NOT updated.
    print("\n" + "="*50)
    print("Scenario 2: Real-time system status changes, but AGENTS.md becomes stale.")
    update_realtime_system_status("maintenance") # Simulate a real-time status change
    # AGENTS_MD_CONTENT remains unchanged, simulating it being stale.

    # Agent Alpha (static) will make a wrong decision
    agent_task_based_on_static_info("Agent Alpha", static_agent_info) # Still uses old static_agent_info

    # Agent Beta (dynamic) will detect the discrepancy and make the correct decision
    agent_task_with_dynamic_validation("Agent Beta", static_agent_info)

    print("\n--- Simulation End ---")
