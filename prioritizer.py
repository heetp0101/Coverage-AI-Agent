import json

def calculate_priority_score(sug):
    # 1. Coverage Impact (Weight: 0.4)
    impact_map = {"High": 10, "Medium": 5, "Low": 2}
    impact = impact_map.get(sug['priority'], 5)
    
    # 2. Inverse Difficulty (Weight: 0.3)
    # Mapping: Easy=1, Medium=2, Hard=3. Formula: (1/Difficulty)
    diff_map = {"Easy": 1, "Medium": 2, "Hard": 3}
    difficulty_val = diff_map.get(sug['difficulty'], 2)
    inv_difficulty = 1 / difficulty_val
    
    # 3. Dependency Score (Weight: 0.3)
    # 1.0 if no dependencies, 0.5 if they exist
    dep_score = 1.0 if len(sug['dependencies']) == 0 else 0.5
    
    # Final Formula
    score = (impact * 0.4) + (inv_difficulty * 0.3) + (dep_score * 0.3)
    return round(score, 2)

def prioritize_suggestions(gemini_json):
    suggestions = gemini_json["suggestions"]
    
    for sug in suggestions:
        sug["priority_score"] = calculate_priority_score(sug)
    
    # Sort suggestions: Highest score first
    sorted_suggestions = sorted(suggestions, key=lambda x: x["priority_score"], reverse=True)
    
    return sorted_suggestions

# --- Let's test it with your data ---
if __name__ == "__main__":
    # Paste the suggestions list you got from Gemini here
    raw_data = {
  "suggestions": [
    {
      "target_bin": "cg_transfer_size.cp_size[max]",
      "priority": "High",
      "difficulty": "Medium",
      "suggestion": "Add a test case to cover the maximum transfer size of 4096.",
      "test_outline": [
        "Configure DMA controller for a transfer.",
        "Set transfer size to 4096 bytes.",
        "Initiate the transfer.",
        "Verify the transfer completes successfully.",
        "Monitor bus activity to ensure the correct amount of data is transferred."
      ],
      "dependencies": [],
      "reasoning": "The 'max[4096]' bin in 'cg_transfer_size.cp_size' is uncovered, indicating that tests for the largest transfer size are missing. This could lead to issues with large data block transfers."    
    },
    {
      "target_bin": "cg_transfer_size.cp_burst_type[wrap]",
      "priority": "Medium",
      "difficulty": "Low",
      "suggestion": "Add a test case specifically for the 'wrap' burst type.",
      "test_outline": [
        "Configure DMA controller for a transfer.",
        "Set burst type to 'wrap'.",
        "Initiate the transfer.",
        "Verify the transfer completes successfully.",
        "Observe burst behavior to ensure it follows the 'wrap' pattern."
      ],
      "dependencies": [],
      "reasoning": "The 'wrap' burst type for 'cg_transfer_size.cp_burst_type' is uncovered. This burst mode might have specific timing or control signal requirements that need verification."
    },
    {
      "target_bin": "cg_channel_arbitration.cp_active_channels[four_channels]",
      "priority": "High",
      "difficulty": "Medium",
      "suggestion": "Create a test scenario where exactly four channels are active.",
      "test_outline": [
        "Configure DMA controller to support 8 channels.",
        "Activate channels 0, 1, 2, and 3.",
        "Initiate transfers on all active channels concurrently.",
        "Verify that arbitration functions correctly and all transfers are eventually serviced.",
        "Monitor channel status signals."
      ],
      "dependencies": [],
      "reasoning": "The 'four_channels' bin for 'cp_active_channels' in 'cg_channel_arbitration' is uncovered. Testing with a specific number of active channels is crucial for verifying the arbitration logic under load."
    },
    {
      "target_bin": "cg_channel_arbitration.cp_active_channels[all_eight]",
      "priority": "High",
      "difficulty": "High",
      "suggestion": "Add a test case that activates all eight channels simultaneously.",
      "test_outline": [
        "Configure DMA controller to support 8 channels.",
        "Activate all eight channels (0-7).",
        "Initiate transfers on all active channels concurrently.",
        "Verify that the arbitration logic handles maximum concurrent requests correctly.",
        "Ensure no starvation occurs for any channel.",
        "Monitor channel status and transfer completion for all channels."
      ],
      "dependencies": [],
      "reasoning": "The 'all_eight' bin for 'cp_active_channels' in 'cg_channel_arbitration' is uncovered. This is a critical scenario for stress-testing the arbitration logic under maximum load."
    },
    {
      "target_bin": "cross_size_burst[small, wrap]",
      "priority": "Medium",
      "difficulty": "Medium",
      "suggestion": "Test a small transfer size combined with the 'wrap' burst type.",
      "test_outline": [
        "Configure DMA controller for a transfer.",
        "Set transfer size to a small value (e.g., 128 bytes).",
        "Set burst type to 'wrap'.",
        "Initiate the transfer.",
        "Verify the transfer completes successfully.",
        "Observe burst behavior to ensure it follows the 'wrap' pattern for small transfers."
      ],
      "dependencies": [
        "cg_transfer_size.cp_burst_type[wrap]"
      ],
      "reasoning": "This cross-coverage scenario was explicitly listed as uncovered. It combines a small transfer size with the 'wrap' burst type, which needs verification to ensure proper interaction."
    },
    {
      "target_bin": "cross_size_burst[medium, wrap]",
      "priority": "Medium",
      "difficulty": "Medium",
      "suggestion": "Test a medium transfer size combined with the 'wrap' burst type.",
      "test_outline": [
        "Configure DMA controller for a transfer.",
        "Set transfer size to a medium value (e.g., 512 bytes).",
        "Set burst type to 'wrap'.",
        "Initiate the transfer.",
        "Verify the transfer completes successfully.",
        "Observe burst behavior to ensure it follows the 'wrap' pattern for medium transfers."
      ],
      "dependencies": [
        "cg_transfer_size.cp_burst_type[wrap]"
      ],
      "reasoning": "This cross-coverage scenario was explicitly listed as uncovered. It combines a medium transfer size with the 'wrap' burst type, which needs verification to ensure proper interaction."
    },
    {
      "target_bin": "cross_size_burst[medium, fixed]",
      "priority": "Medium",
      "difficulty": "Low",
      "suggestion": "Test a medium transfer size combined with the 'fixed' burst type.",
      "test_outline": [
        "Configure DMA controller for a transfer.",
        "Set transfer size to a medium value (e.g., 768 bytes).",
        "Set burst type to 'fixed'.",
        "Initiate the transfer.",
        "Verify the transfer completes successfully.",
        "Observe burst behavior to ensure it follows the 'fixed' pattern for medium transfers."
      ],
      "dependencies": [],
      "reasoning": "This cross-coverage scenario was explicitly listed as uncovered. It combines a medium transfer size with the 'fixed' burst type. While 'fixed' might be the default or implied, explicit testing is good practice."
    }
  ]
}
    
    final_results = prioritize_suggestions(raw_data)
    
    print(f"{'Target Bin':<40} | {'Score':<10}")
    print("-" * 55)
    for item in final_results:
        print(f"{item['target_bin']:<40} | {item['priority_score']:<10}")