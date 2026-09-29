from .graph import build_graph

app = build_graph()

result = app.invoke({
    "question": "Define AI",
})

print("\n\nResult for Tool-Using Agent:")
print(result)
