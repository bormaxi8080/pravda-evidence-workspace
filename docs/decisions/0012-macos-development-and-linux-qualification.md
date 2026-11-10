# ADR-012: Develop on macOS; qualify Linux separately

Date: 2026-11-10. Status: **adopted platform and delivery policy; runtime
qualification remains evidence-dependent**. Authority: the operator requested
macOS development, a separate Linux iteration, updated requirements/tasks and a commit.

## Problem

The Linux preparation dependency blocked images and all their dependants before
local development. Deferring provisioning without changing that dependency's
meaning did not unblock work. LOC-4 did produce code; its review/integration
obligations are independent of platform availability.

## Decision

Select MAC-DEV as the current implementation lane: this macOS arm64 machine,
Python 3.12, PostgreSQL 16, and Docker Desktop Linux arm64 containers where needed.
Native developer tools and real local browser/API/database checks are supported.
Record actual versions, architectures, guest kernel, images, resource allocations
and storage/network behavior; do not invent supported capacities or pins.

Select LINUX-QUAL as a separate later, explicitly admitted iteration on native
Linux x86_64/Ubuntu 24.04. Its target builds, isolation, installation and recovery
checks are prerequisites for Linux support/production claims, not for Mac coding,
local tests, review or implementation completion. Emulated amd64 builds on Mac are
portability diagnostics, not native target qualification.

Retain all 170 requirement IDs, 78 EWP IDs and 76 scenario definitions. Current
EWP tickets become MAC-DEV implementation tickets; separate Linux orchestration
tickets retain native-target evidence obligations. A local done status means
accepted/integrated implementation in this lane, not universal qualification.

Retarget PC-SETUP-03/LOC-3 to the Mac environment, preserve its old Linux reports,
supersede the obsolete Linux question and move that work to Linux backlog tickets.
Preserve EWP dependencies and human reviews, including LOC-4's existing delivered
commit and pending whole-package review. Do not accept code through a planning update.

## Limits and precedence

Privacy, authorization, immutable original bytes, safe rendering and resource
bounds apply in both lanes. Browser/decoder processes receive no Docker socket,
DB credentials or final-store writes. Real local failures are not passing evidence;
keep affected capture features off and continue independent trusted synthetic work.
Missing local access is an exact Mac bootstrap action, not a Linux-host request.

This supersedes only initial-platform sequencing in ADR-002/009/011 and documents
09/13/17/44/49/55. Product release/date remain null. Detailed scope, ticket gates
and Linux handoff are in [document 56](../requirements/56-macos-development-and-linux-qualification.md)
and the [Mac runbook](../operations/macos-development.md).
