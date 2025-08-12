import inspect
import src.fetch as F

print("USING:", F.__file__)
print("\n--- fetch() source ---")
print(inspect.getsource(F.fetch))

print("\n--- calling fetch(debug=True) ---")
hits = F.fetch(debug=True)
print("HITS:", len(hits))
