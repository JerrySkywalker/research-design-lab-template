import FormalExample
import Lean

open Lean Elab Command Meta

namespace StatementLock

def expectedOddSum : Nat → Nat :=
  Nat.rec 0 (fun n total => total + (2 * n + 1))

def expectedStatement : Prop :=
  ∀ n : Nat, expectedOddSum n = n ^ 2

-- Check the actual type and cited definition body in the imported environment.
-- Full transparency compares the independently written lock with the compiled values.
run_cmd liftTermElabM do
  let env ← getEnv
  let allowedModules := [`FormalExample, `FormalExample.OddSum]
  for name in allowedModules do
    unless env.header.moduleNames.contains name do
      throwError "missing accepted module {name}"
  for name in env.header.moduleNames do
    let root := name.getRoot
    if (root == `FormalExample && !allowedModules.contains name) ||
       root == `Drafts || root == `Challenges then
      throwError "unexpected module in accepted import graph: {name}"

  let theoremName := `FormalExample.oddSum_eq_square
  let definitionName := `FormalExample.oddSum
  let some (.thmInfo theoremInfo) := env.find? theoremName
    | throwError "missing accepted theorem {theoremName}"
  let some (.defnInfo definitionInfo) := env.find? definitionName
    | throwError "missing accepted definition {definitionName}"
  let some (.defnInfo lockedDefinition) := env.find? `StatementLock.expectedOddSum
    | throwError "missing locked definition"
  let some (.defnInfo lockedStatement) := env.find? `StatementLock.expectedStatement
    | throwError "missing locked statement"
  unless ← withTransparency .all (isDefEq definitionInfo.value lockedDefinition.value) do
    throwError "locked definition changed"
  unless ← withTransparency .all (isDefEq theoremInfo.type lockedStatement.value) do
    throwError "locked statement changed"

  let allowedAxioms := [`propext, `Classical.choice, `Quot.sound]
  let exported := env.constants.toList.filterMap fun (name, _) =>
    match env.getModuleIdxFor? name with
    | some idx =>
      if allowedModules.contains env.header.moduleNames[idx.toNat]! then some name else none
    | none => none
  unless exported.contains definitionName && exported.contains theoremName do
    throwError "incomplete accepted declaration inventory"
  for name in exported do
    let axioms ← Lean.collectAxioms name
    for axiomName in axioms do
      unless allowedAxioms.contains axiomName do
        throwError "unapproved axiom {axiomName} in {name}"
    logInfo m!"{name} axioms: {axioms.toList}"

end StatementLock
