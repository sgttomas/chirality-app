# analysis-binding: checks before freezing

1. **Method.** Every analysis names its method. The method's applicability was checked against the actual data contract, and any unmet condition became a choice, a caveat or a returned finding.
2. **Parameters.** Every parameter value has grounds and standing; unknown values are TBD with a gap.
3. **Interface.** Every binding names only declared ports and parameters; the semantic validator's R-IF1 check passes.
4. **Result semantics.** These are stated wherever meaning depends on more than the interface.
5. **Tests.** Every component has the known-answer tests its tier requires (data-app-spec gates). Each test has an oracle independent of the component, a tolerance rationale and a confirmation status.
6. **Boundary cases.** These are tested, and the user-facing message for each precondition failure exists.
7. **Versions.** They are pinned. Version-behaviour differences that matter are recorded.
8. **Examination.** A separate agent examined the binding. Domain and independent-verification reviews required by the tier are complete or stated as blocking.
9. **New components.** Each has a specification with interface, behaviour cases and acceptance verification ready for decomposition.
