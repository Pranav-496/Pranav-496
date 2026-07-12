import re

file_path = "d:\\Pranav-496\\github-user-contribution.svg"
with open(file_path, "r", encoding="utf-8") as f:
    svg = f.read()

# Replace variables
# We want dark luxury theme:
# --cb (border): #1b1f230a -> rgba(255,255,255,0.05)
# --ce (empty): #0D1117 -> #1E1E2E
# --c0 (lowest): -> #1E1E2E
# --c1 (low): -> #4C1D95
# --c2 (med): -> #6D28D9
# --c3 (high): -> #8B5CF6
# --c4 (highest): -> #A855F7
# --cs (snake): url(#snake-grad)

css_vars = "--cb:rgba(255,255,255,0.05);--cs:url(#snake-grad);--ce:#1E1E2E;--c0:#1E1E2E;--c1:#4C1D95;--c2:#6D28D9;--c3:#8B5CF6;--c4:#A855F7"
svg = re.sub(r':root\{[^\}]+\}', f":root{{{css_vars}}}", svg)

# Inject defs right after <svg ...>
defs = """<defs>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0D1117"/>
        <stop offset="100%" stop-color="#12121E"/>
    </linearGradient>
    <linearGradient id="snake-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#A855F7"/>
        <stop offset="100%" stop-color="#6366F1"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="3" result="blur1" />
        <feGaussianBlur stdDeviation="8" result="blur2" />
        <feMerge>
            <feMergeNode in="blur2"/>
            <feMergeNode in="blur1"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>
</defs>"""

# Add background rect
# Find viewBox to set background properly if needed, but 100% width/height is easier
svg = re.sub(r'(<svg[^>]*>)', r'\1' + defs + '<rect width="100%" height="100%" fill="url(#bg-grad)" x="-5%" y="-5%" rx="16"/>', svg, count=1)

# Modify `.s` (the snake) to have a glow and look like particles
# We can just add filter:url(#glow)
# If it's a stroke, we could make it dashed, but in snk SVG, the snake is actually composed of SVG <path> or <g> shapes (usually filled, not stroked).
# We can just add the glow filter to it.
svg = svg.replace('.s{', '.s{filter:url(#glow);')
svg = svg.replace('.c{', '.c{rx:4;ry:4;') # More rounded cells

with open(file_path, "w", encoding="utf-8") as f:
    f.write(svg)
print("Themed successfully.")
