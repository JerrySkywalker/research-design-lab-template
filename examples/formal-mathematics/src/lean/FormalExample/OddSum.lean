import Mathlib.Tactic.Ring

namespace FormalExample

/-- Sum of the first n positive odd natural numbers, starting at 1. -/
def oddSum : Nat → Nat :=
  Nat.rec 0 (fun n total => total + (2 * n + 1))

theorem oddSum_eq_square (n : Nat) : oddSum n = n ^ 2 := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change oddSum n + (2 * n + 1) = (n + 1) ^ 2
    rw [ih]
    ring

end FormalExample
