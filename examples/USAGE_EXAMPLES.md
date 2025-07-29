# Usage Examples

This document provides practical examples of how to use the Gemini AI Discord Bot effectively.

## Basic Chat Examples

### Simple Questions
```
User: !gemini What is the capital of Japan?
Bot: The capital of Japan is Tokyo. Tokyo has been the capital since 1868 and is the largest metropolitan area in the world...

User: !ai Explain photosynthesis
Bot: Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen...
```

### Creative Writing
```
User: !chat Write a short story about a robot learning to paint
Bot: In a small workshop filled with gears and circuits, R-7 discovered an old paintbrush. Unlike its usual tasks of welding and assembly...

User: !gemini Create a haiku about coding
Bot: Lines of code flow like
Rivers through digital minds—
Logic becomes art
```

### Conversation Memory
```
User: !gemini My name is Alex and I love pizza
Bot: Nice to meet you, Alex! Pizza is definitely a great choice. What's your favorite type of pizza?

User: !gemini What did I tell you about myself?
Bot: You told me that your name is Alex and that you love pizza! Do you have a favorite pizza topping?
```

## Image Analysis Examples

### Basic Image Description
```
User: !vision [uploads image of a sunset]
Bot: This image shows a beautiful sunset over what appears to be a body of water. The sky is painted in warm hues of orange, pink, and purple...

User: !image What colors do you see? [uploads abstract art]
Bot: I can see a vibrant mix of colors including deep blues, bright yellows, crimson reds, and forest greens...
```

### Specific Questions
```
User: !analyze How many people are in this photo? [uploads group photo]
Bot: I can see 5 people in this photograph. They appear to be standing together in what looks like a casual group setting...

User: !see What breed of dog is this? [uploads dog photo]
Bot: Based on the features I can observe, this appears to be a Golden Retriever. The dog has the characteristic...
```

## Translation Examples

### Basic Translation
```
User: !translate Spanish Hello, how are you today?
Bot: 🌐 Translation to Spanish
Hola, ¿cómo estás hoy?

Original Text: Hello, how are you today?

User: !trans French I love programming
Bot: 🌐 Translation to French
J'adore la programmation

Original Text: I love programming
```

### Complex Sentences
```
User: !translate Japanese The weather is beautiful today, perfect for a picnic in the park
Bot: 🌐 Translation to Japanese
今日は天気が美しく、公園でピクニックをするのに最適です

Original Text: The weather is beautiful today, perfect for a picnic in the park
```

## Code Generation Examples

### Python Examples
```
User: !code python function to calculate fibonacci sequence
Bot: ```python
def fibonacci(n):
    """
    Calculate the nth Fibonacci number
    Args: n (int): The position in the sequence
    Returns: int: The Fibonacci number at position n
    """
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Example usage
print(fibonacci(10))  # Output: 55
```

User: !generate python sort a list of dictionaries by age
Bot: ```python
# Sort list of dictionaries by age
people = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
]

# Sort by age (ascending)
sorted_people = sorted(people, key=lambda x: x["age"])
print(sorted_people)

# Sort by age (descending)
sorted_desc = sorted(people, key=lambda x: x["age"], reverse=True)
```
```

### JavaScript Examples
```
User: !code javascript async function to fetch data from API
Bot: ```javascript
/**
 * Fetch data from an API endpoint
 * @param {string} url - The API endpoint URL
 * @returns {Promise<Object>} - The response data
 */
async function fetchData(url) {
    try {
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
}

// Example usage
fetchData('https://api.example.com/data')
    .then(data => console.log(data))
    .catch(error => console.error(error));
```
```

## Text Summarization Examples

### Article Summary
```
User: !summarize [long article about climate change...]
Bot: 📄 Text Summary

This article discusses the current state of climate change and its impacts on global ecosystems. Key points include:

• Rising global temperatures have increased by 1.1°C since pre-industrial times
• Arctic ice is melting at an accelerated rate
• Extreme weather events are becoming more frequent
• Renewable energy adoption is crucial for mitigation
• International cooperation is needed for effective solutions

Original Text: [long article about climate change...]
```

### Meeting Notes
```
User: !summary [meeting transcript about project planning...]
Bot: 📄 Text Summary

Meeting focused on Q1 project planning with the following decisions:

• Project deadline set for March 31st
• Team will use Agile methodology
• Weekly sprints starting Monday
• Budget approved for additional resources
• Next review meeting scheduled for January 15th

Original Text: [meeting transcript about project planning...]
```

## Image Prompt Optimization Examples

### Basic Optimization
```
User: !imagine a cat sitting on a rainbow
Bot: 🎨 Image Generation Prompt

**Optimized Prompt:**
A fluffy domestic cat with detailed fur texture sitting gracefully on a vibrant rainbow arc, soft natural lighting, high detail, photorealistic style, beautiful composition, 4K quality

**Style Suggestions:**
- Photorealistic digital art
- Whimsical illustration style
- Studio Ghibli anime style

**Additional Keywords:**
- "detailed fur texture"
- "vibrant colors"
- "magical atmosphere"
```

### Complex Scene
```
User: !prompt futuristic city at sunset with flying cars
Bot: 🎨 Image Generation Prompt

**Optimized Prompt:**
Futuristic cyberpunk cityscape at golden hour sunset, towering glass skyscrapers with neon lights, sleek flying cars with glowing trails in the sky, dramatic orange and purple sunset clouds, detailed architecture, cinematic composition, ultra-wide angle, 8K resolution, concept art style

**Style Suggestions:**
- Cyberpunk concept art
- Blade Runner aesthetic
- Digital matte painting

**Additional Keywords:**
- "volumetric lighting"
- "atmospheric perspective"
- "sci-fi architecture"
```

## Admin Commands Examples

### Bot Statistics
```
Admin: !stats
Bot: 📊 Bot Statistics

Users with conversation history: 47
Total conversation messages: 1,234
Servers: 3
```

### Temperature Adjustment
```
Admin: !temperature 0.9
Bot: ✅ Temperature value set to 0.9.

Admin: !temp
Bot: ℹ️ Current temperature value: 0.9
```

### Bulk Reset
```
Admin: !reset_all
Bot: ✅ All conversation histories have been reset.
```

## Cooldown Management Examples

### Checking Status
```
User: !cooldown_status
Bot: ⏰ Your Cooldown Status

!gemini: ✅ Ready
!vision: ⏳ 2.3s remaining
!translate: ✅ Ready
!summarize: ✅ Ready
!code: ⏳ 1.7s remaining
!imagine: ✅ Ready
```

### Cooldown Messages
```
User: !gemini Hello again
Bot: ⏰ Command is on cooldown. Try again in 2s.

User: !vision [uploads image]
Bot: ⏰ Command is on cooldown. Try again in 4s.
```

## Error Handling Examples

### Input Validation
```
User: !translate
Bot: Usage: !translate [target language] [text]

User: !gemini [extremely long text...]
Bot: ❌ Prompt is too long. Maximum length: 4000 characters.

User: !vision [uploads 50MB image]
Bot: ❌ Image too large. Maximum size: 20MB
```

### API Errors
```
User: !gemini What is AI?
Bot: ❌ API quota exceeded. Please try again later.

User: !vision [uploads image]
Bot: ❌ Network error. Please check your connection and try again.
```

## Best Practices

### Effective Prompting
- **Be specific**: "Explain quantum computing for beginners" vs "What is quantum computing?"
- **Provide context**: "Write a Python function that..." vs "Write a function..."
- **Ask follow-ups**: Use conversation memory to build on previous responses

### Image Analysis Tips
- **High quality images**: Better results with clear, well-lit images
- **Specific questions**: "What breed is this dog?" vs "Analyze this image"
- **Multiple angles**: Try different views of the same object

### Translation Best Practices
- **Simple sentences**: Break complex text into smaller parts
- **Context matters**: Provide context for ambiguous terms
- **Verify results**: Double-check important translations

---

These examples should help you get the most out of your Gemini AI Discord Bot! Experiment with different prompts and commands to discover what works best for your needs.
