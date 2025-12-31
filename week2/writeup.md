# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt:
```
Analyze the existing extract_action_items() function in week2/app/services/extract.py, which currently extracts action items using predefined heuristics.

Implement an LLM-powered alternative, extract_action_items_llm(), that utilizes Ollama to perform action item extraction via a large language model.

Requirements:
- Use Ollama's structured outputs (format="json") to get a JSON array of strings
- Handle empty input gracefully
- Parse different JSON response formats (list or dict with action_items/items key)
- Include error handling for JSON parsing failures
- Use llama3.2:3b model by default with low temperature for consistency
```

Generated Code Snippets:
```
week2/app/services/extract.py: lines 92-157

Added extract_action_items_llm() function that:
- Takes text input and optional model parameter
- Returns empty list for empty/whitespace input
- Uses system prompt instructing LLM to extract action items as JSON array
- Calls Ollama chat() with format="json" for structured output
- Parses JSON response handling both list and dict formats
- Includes error handling for JSONDecodeError and other exceptions
```

### Exercise 2: Add Unit Tests
Prompt:
```
Write unit tests for extract_action_items_llm() covering multiple inputs:
- Bullet lists (-, *, •)
- Keyword-prefixed lines (TODO:, Action:, Next:)
- Checkbox items ([ ], [x])
- Empty input
- No action items (non-actionable text)
- Mixed content (actionable + non-actionable)
- Numbered lists (1., 2., 3.)

Use pytest and ensure tests verify:
- Function returns a list
- All items are strings
- Empty input returns empty list
```

Generated Code Snippets:
```
week2/tests/test_extract.py: lines 22-119

Added TestExtractActionItemsLLM class with 8 test methods:
- test_extract_bullet_list: Tests bullet point extraction
- test_extract_keyword_prefixed_lines: Tests TODO/Action prefix extraction
- test_extract_checkbox_items: Tests checkbox-style items
- test_empty_input: Verifies empty/whitespace returns []
- test_no_action_items: Tests non-actionable text handling
- test_mixed_content: Tests mixed actionable/non-actionable content
- test_returns_list: Verifies return type is always list
- test_numbered_list: Tests numbered list extraction

Also fixed extract.py line 148 to handle "actionItems" camelCase key from LLM response.
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
TODO
``` 

Generated/Modified Code Snippets:
```
TODO: List all modified code files with the relevant line numbers. (We anticipate there may be multiple scattered changes here – just produce as comprehensive of a list as you can.)
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 