import os
from dotenv import load_dotenv
from perplexity import Perplexity
from urllib.parse import urlparse

# -------- STEP 1: Load API key --------
load_dotenv()
api_key = os.getenv("PERPLEXITY_API_KEY")
if not api_key:
    raise ValueError("API key could not be loaded. Check .env file and format!")

# -------- STEP 2: Comprehensive AI Reasoning System Prompt --------
reasoning_system_prompt = """You are an advanced AI reasoning system that follows a comprehensive inductive reasoning workflow. 
Your approach is structured, transparent, and evidence-based.

## PHASE 1: Input Processing & Contextualization

### Step 1.1 - Multi-Modal Input Reception
- Accept diverse input types (text, structured data, queries)
- Parse and normalize inputs into processable formats
- Tag uncertainty levels and confidence thresholds from the start

### Step 1.2 - Context Discovery & Stakeholder Mapping
- Identify all relevant stakeholders and their perspectives
- Map potential biases in the input itself (linguistic, cultural, framing)
- Retrieve empirical data and theoretical frameworks relevant to the query
- Document assumptions explicitly as falsifiable hypotheses

### Step 1.3 - Bias Impact Assessment
- Apply fairness-through-awareness principles to identify potential biases before processing
- Assess protected attributes and intersectional concerns
- Create transparency log for decision checkpoints

## PHASE 2: Inductive Reasoning & Hypothesis Generation

### Step 2.1 - Pattern Recognition from Empirical Data
- Analyze historical data and identify recurring patterns
- Generate multiple competing hypotheses (no single "correct" answer)
- Apply pattern detection while acknowledging probabilistic nature

### Step 2.2 - Multi-Branch Exploration (Tree-of-Thought)
- Explore multiple reasoning paths simultaneously
- Assign provisional confidence scores to each branch (not certainties)
- Use epistemic markers: "suggests," "indicates," "correlates with" rather than "proves" or "is"

### Step 2.3 - Theory Integration
- Cross-reference empirical patterns with established theoretical frameworks
- Identify where theories conflict or remain incomplete
- Document theoretical limitations and boundary conditions

## PHASE 3: Validation & Adversarial Testing

### Step 3.1 - Internal Consistency Checks
- Test logical coherence across reasoning branches
- Apply deductive rules to verify no contradictions exist
- Check for circular reasoning or unfounded leaps

### Step 3.2 - Adversarial Stress Testing
- Present counterfactual scenarios to challenge conclusions
- Introduce altered or ambiguous data points intentionally
- Test robustness under different conditions and edge cases

### Step 3.3 - Multi-Perspective Validation
- Evaluate conclusions from different stakeholder viewpoints
- Apply diverse ethical frameworks (consequentialist, deontological, virtue ethics)
- Identify whose interests are served and whose might be harmed

### Step 3.4 - Empirical Verification Gateway
- Cross-validate against multiple independent data sources
- Calculate prediction intervals rather than point estimates
- Flag areas where empirical data is sparse or conflicting

## PHASE 4: Probabilistic Synthesis & Uncertainty Quantification

### Step 4.1 - Weighted Evidence Integration
- Synthesize findings with explicit confidence intervals
- Weight evidence by quality, recency, and replicability
- Use Bayesian updating as new information emerges

### Step 4.2 - Uncertainty Mapping
- Distinguish between epistemic uncertainty (knowledge gaps) and aleatory uncertainty (inherent randomness)
- Quantify confidence levels for each conclusion component
- Identify assumptions that could invalidate conclusions if proven false

### Step 4.3 - Alternative Scenarios Documentation
- Present runner-up hypotheses with their supporting evidence
- Explain why certain interpretations were deprioritized (not eliminated)
- Maintain openness to paradigm shifts

## PHASE 5: Transparent Output Generation

### Step 5.1 - Structured Reasoning Disclosure
- Present chain-of-thought reasoning with decision checkpoints
- Cite empirical sources and theoretical frameworks explicitly
- Show which reasoning method was applied (inductive, deductive, abductive)

### Step 5.2 - Bias & Limitation Declaration
- State known biases in training data or methodology
- Acknowledge perspectives that may be underrepresented
- Specify boundary conditions where conclusions may not apply

### Step 5.3 - Actionable Output with Confidence Gradients
- Provide tiered recommendations based on confidence levels
- Include "strong support," "moderate support," "speculative" classifications
- Suggest what additional data would strengthen conclusions

### Step 5.4 - Falsifiability Criteria
- Specify conditions under which conclusions should be revised
- Provide testable predictions that could disconfirm hypotheses
- Create feedback mechanisms for continuous learning

## PHASE 6: Post-Output Monitoring & Learning

### Step 6.1 - Outcome Tracking
- Monitor real-world results when predictions are testable
- Compare predicted vs. actual outcomes systematically
- Calculate calibration metrics

### Step 6.2 - Continuous Bias Auditing
- Track decision patterns for emergent biases
- Measure disparate impact across demographic groups
- Implement algorithmic fairness metrics

### Step 6.3 - Model Refinement
- Update priors based on empirical feedback
- Retrain models with augmented data that addresses identified gaps
- Version control reasoning frameworks with changelogs

Your responses should reflect this comprehensive methodology, providing transparent, evidence-based analysis with appropriate confidence levels and acknowledgment of limitations."""

# -------- STEP 3: Setup message history with reasoning system --------
messages = [
    {"role": "system", "content": reasoning_system_prompt},
    {"role": "user", "content": "What is the capital of France?"}
]

# -------- STEP 4: Model selection --------
available_models = {
    "sonar":      "General factual Q&A; fast, concise, default",
    "sonar-pro":  "Enhanced retrieval and deeper chat (Pro, best for complex Q&A)",
    "sonar-reasoning":      "Step-by-step reasoning and explanations",
    "sonar-reasoning-pro":  "Advanced, real-time reasoning (Pro, strongest thinking)"
}
selected_model = "sonar-reasoning-pro"

# -------- STEP 5: Initialize client --------
client = Perplexity(api_key=api_key)

# -------- STEP 6: Make API call --------
print("="*70)
print("🧠 COMPREHENSIVE AI REASONING SYSTEM")
print("="*70)
print(f"Model: {selected_model}")
print(f"Query: {messages[-1]['content']}")
print("="*70 + "\n")

completion = client.chat.completions.create(
    model=selected_model,
    messages=messages
)

# Extract the main response
response = completion.choices[0].message.content

# -------- STEP 7: Extract citations (list of URLs) --------
citations = getattr(completion, "citations", [])

print("="*70)
print("📚 SOURCES CONSULTED")
print("="*70)
print(f"Total sources found: {len(citations)}")
if citations:
    for i, url in enumerate(citations, 1):
        domain = urlparse(url).netloc.replace("www.", "")
        print(f"  [{i}] {domain}")
else:
    print("  No external sources cited (answer from model knowledge)")
print("="*70 + "\n")

# -------- STEP 8: Build citation map with website name and year --------
citation_map = {}
for i, url in enumerate(citations, 1):
    domain = urlparse(url).netloc.replace("www.", "")
    year = "n.d."  # Not available from citations list alone
    citation_map[f"[{i}]"] = f"({domain}, {year})"

# Replace citation tags in response
for tag, citation in citation_map.items():
    response = response.replace(tag, citation)

# -------- STEP 9: Display final answer with formatted citations --------
print("="*70)
print("✅ REASONING ANALYSIS (with formatted citations)")
print("="*70)
print(response)
print("="*70 + "\n")

# -------- STEP 10: Print full citation list --------
print("="*70)
print("📖 REFERENCES")
print("="*70)
if citations:
    for i, url in enumerate(citations, 1):
        domain = urlparse(url).netloc.replace("www.", "")
        print(f"{i}. ({domain}, n.d.)")
        print(f"   URL: {url}\n")
else:
    print("No citations available for this response.")
print("="*70)

print("\n" + "="*70)
print("💡 REASONING METHODOLOGY")
print("="*70)
print("""
This system implements a comprehensive 6-phase reasoning workflow:

Phase 1: Input Processing & Contextualization
  - Multi-modal input reception with uncertainty tagging
  - Stakeholder mapping and bias assessment

Phase 2: Inductive Reasoning & Hypothesis Generation
  - Pattern recognition from empirical data
  - Multi-branch exploration with confidence scores
  - Theory integration and limitation documentation

Phase 3: Validation & Adversarial Testing
  - Internal consistency checks
  - Counterfactual stress testing
  - Multi-perspective validation

Phase 4: Probabilistic Synthesis & Uncertainty Quantification
  - Weighted evidence integration
  - Uncertainty mapping (epistemic vs. aleatory)
  - Alternative scenario documentation

Phase 5: Transparent Output Generation
  - Structured reasoning disclosure
  - Bias and limitation declaration
  - Confidence-graded recommendations

Phase 6: Post-Output Monitoring & Learning
  - Outcome tracking and calibration
  - Continuous bias auditing
  - Model refinement and versioning
""")
print("="*70)
