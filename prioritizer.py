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

      "target_bin": "cg_transfer_size.cp_size.max[4096]",

      "priority": "High",

      "difficulty": "Medium",

      "suggestion": "Add a test case to specifically target the maximum transfer size of 4096.",

      "test_outline": [

        "Configure the DMA controller for a transfer.",

        "Set the transfer size to exactly 4096.",

        "Initiate the transfer and verify successful completion.",

        "Monitor the transfer size register to ensure it accurately reflects 4096."

      ],

      "dependencies": [],

      "reasoning": "The bin 'max[4096]' for cp_size in cg_transfer_size is uncovered, indicating that transfers of this specific size have not been tested. This is a critical boundary condition that needs verification."

    },

    {

      "target_bin": "cg_transfer_size.cp_burst_type.wrap",

      "priority": "Medium",

      "difficulty": "Easy",

      "suggestion": "Introduce test cases that utilize the 'wrap' burst type for transfer sizes.",        

      "test_outline": [

        "Configure the DMA controller for a transfer.",

        "Set the burst type to 'wrap'.",

        "Perform transfers of various sizes (e.g., small, medium, and near 4096).",

        "Verify the wrap-around behavior of the burst transactions if applicable."

      ],

      "dependencies": [],

      "reasoning": "The 'wrap' burst type for cg_transfer_size.cp_burst_type is uncovered. This burst mode needs to be tested to ensure correct behavior."

    },

    {

      "target_bin": "cg_channel_arbitration.cp_active_channels.four_channels",

      "priority": "High",

      "difficulty": "Medium",

      "suggestion": "Create a test scenario where exactly four DMA channels are active simultaneously.",  

      "test_outline": [

        "Configure and enable four distinct DMA channels.",

        "Initiate transfers on all four channels concurrently or in close succession.",

        "Monitor the arbitration logic to ensure fair and correct channel selection.",

        "Verify that all four active channels receive adequate bandwidth and complete their transfers."   

      ],

      "dependencies": [],

      "reasoning": "The scenario with exactly four active channels in cg_channel_arbitration.cp_active_channels is not covered, which is a specific configuration that needs to be validated for correct arbitration."

    },

    {

      "target_bin": "cg_channel_arbitration.cp_active_channels.all_eight",

      "priority": "High",

      "difficulty": "Hard",

      "suggestion": "Develop a test that stresses the arbitration mechanism with all eight DMA channels active.",

      "test_outline": [

        "Configure and enable all eight DMA channels.",

        "Initiate concurrent transfers across all eight channels, potentially with varying sizes and priorities.",

        "Perform extensive monitoring of the arbitration logic under heavy load.",

        "Verify that the system remains stable and that all channels make progress without starvation.",  

        "Analyze performance metrics to ensure acceptable throughput for each channel."

      ],

      "dependencies": [],

      "reasoning": "The 'all_eight' active channels scenario for cg_channel_arbitration.cp_active_channels is uncovered. Testing this maximum load condition is crucial for verifying the robustness and fairness of the arbitration logic."

    },

    {

      "target_bin": "cross_size_burst.small, wrap",

      "priority": "Medium",

      "difficulty": "Easy",

      "suggestion": "Test a small transfer size combined with the 'wrap' burst type.",

      "test_outline": [

        "Configure the DMA controller for a small transfer size.",

        "Set the burst type to 'wrap'.",

        "Initiate the transfer and verify its completion.",

        "Observe burst behavior if applicable."

      ],

      "dependencies": [

        "cg_transfer_size.cp_size.small",

        "cg_transfer_size.cp_burst_type.wrap"

      ],

      "reasoning": "The combination of 'small' transfer size and 'wrap' burst type is missing from the cross-coverage, indicating a gap in testing this specific interaction."

    },

    {

      "target_bin": "cross_size_burst.medium, wrap",

      "priority": "Medium",

      "difficulty": "Easy",

      "suggestion": "Test a medium transfer size combined with the 'wrap' burst type.",

      "test_outline": [

        "Configure the DMA controller for a medium transfer size.",

        "Set the burst type to 'wrap'.",

        "Initiate the transfer and verify its completion.",

        "Observe burst behavior if applicable."

      ],

      "dependencies": [

        "cg_transfer_size.cp_size.medium",

        "cg_transfer_size.cp_burst_type.wrap"

      ],

      "reasoning": "The combination of 'medium' transfer size and 'wrap' burst type is missing from the cross-coverage, indicating a gap in testing this specific interaction."

    },

    {

      "target_bin": "cross_size_burst.medium, fixed",

      "priority": "Medium",

      "difficulty": "Easy",

      "suggestion": "Test a medium transfer size combined with the 'fixed' burst type.",

      "test_outline": [

        "Configure the DMA controller for a medium transfer size.",

        "Set the burst type to 'fixed'.",

        "Initiate the transfer and verify its completion.",

        "Observe burst behavior if applicable."

      ],

      "dependencies": [

        "cg_transfer_size.cp_size.medium",

        "cg_transfer_size.cp_burst_type.fixed"

      ],

      "reasoning": "The combination of 'medium' transfer size and 'fixed' burst type is missing from the cross-coverage, indicating a gap in testing this specific interaction."

    }

  ]

}
    
    final_results = prioritize_suggestions(raw_data)
    
    print(f"{'Target Bin':<40} | {'Score':<10}")
    print("-" * 55)
    for item in final_results:
        print(f"{item['target_bin']:<40} | {item['priority_score']:<10}")