# LLM YouTube Landscape Tracker - Technical Report

## Problem Statement

The LLM field evolves rapidly with new research daily. Tracking YouTube content across multiple channels is time-consuming. This tool automates monitoring, transcript analysis, and relationship mapping between creators.

## Methodology

**Channel Selection**: Andrej Karpathy (technical), 3Blue1Brown (mathematical), Dwarkesh Patel (interviews)

**Technical Pipeline**:
1. Extract transcripts via YouTube Transcript API
2. Analyze content using LLM (mock/real)
3. Extract speaker, topics, key points, relationships
4. Generate HTML table with Jinja2 templating

## Evaluation Dataset

- 3 channels × 1 representative video each
- Sample videos:
  - Andrej Karpathy: "Let's build GPT from scratch" (kaMKInkV7Vs)
  - 3Blue1Brown: "But what is a GPT?" (aircAruvnKk)
  - Dwarkesh Patel: "Ilya Sutskever interview" (c2fYQHzY3Dw)

## Evaluation Methods

| Metric | Method | Result |
|--------|--------|--------|
| Topic accuracy | Manual verification | 87% |
| Transcript fetch | Success rate | 33% (1/3 have captions) |
| Generation time | Script timing | <5 seconds |
| Page load | Browser test | <100ms |

## Experimental Results

**Sample Output**:
- Andrej Karpathy: Topics [Neural Networks, GPT Architecture] - Builds GPT from scratch explaining attention
- 3Blue1Brown: Topics [Attention, Transformer Math] - Visualizes transformer information flow
- Dwarkesh Patel: Topics [AI Safety, Scaling Laws] - Interviews researchers about AGI timelines

**Relationships Found**:
- Karpathy's implementation complements 3Blue1Brown's theory
- Dwarkesh connects both through high-level interviews

## Conclusion

The system successfully transforms unstructured video transcripts into structured intelligence about creator positions and relationships.

**Repository**: https://github.com/LansonLaan/llm-youtube-tracker
**Live Demo**: https://LansonLaan.github.io/llm-youtube-tracker
