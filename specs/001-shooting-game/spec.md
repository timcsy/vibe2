# Feature Specification: 射擊遊戲 (Shooting Game)

**Feature Branch**: `001-shooting-game`
**Created**: 2026-03-06
**Status**: Draft
**Input**: User description: "射擊遊戲"

## Overview

A 2D arcade-style shooting game where players control a character or vehicle to defeat waves of enemies by shooting projectiles, earning points, and surviving as long as possible. The game delivers a fast-paced, engaging experience playable directly in a web browser without any installation.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Play a Complete Game Session (Priority: P1)

A player visits the game, starts a new session, controls their character to shoot incoming enemies, loses lives when hit, and the session ends when all lives are lost or the player clears all waves. The player sees their final score at the end.

**Why this priority**: This is the core gameplay loop. Without it, nothing else has value. It is the MVP: a playable, start-to-finish game session.

**Independent Test**: Can be fully tested by launching the game, playing from start to game-over, and verifying the score screen is displayed.

**Acceptance Scenarios**:

1. **Given** the game has loaded on the main screen, **When** the player presses the start button, **Then** the game begins with the player's character visible, enemies appearing, and the score set to zero.
2. **Given** the game is running, **When** the player fires a projectile that hits an enemy, **Then** the enemy is destroyed and the score increases by the enemy's point value.
3. **Given** the player has one remaining life, **When** an enemy projectile or enemy collides with the player, **Then** the game ends and the game-over screen displays the final score.
4. **Given** the game-over screen is displayed, **When** the player selects "Play Again", **Then** a new game session begins with the score and lives reset to their starting values.

---

### User Story 2 - Navigate Player and Shoot (Priority: P1)

A player uses keyboard or touch controls to move their character across the game area and fire projectiles at enemies in real time.

**Why this priority**: Core interactivity of the game. Without responsive controls, the game is unplayable.

**Independent Test**: Can be tested in isolation by starting a game and verifying the character moves in all supported directions and fires projectiles on command.

**Acceptance Scenarios**:

1. **Given** the game is running, **When** the player presses the movement keys (e.g., arrow keys or WASD), **Then** the player's character moves smoothly in the corresponding direction within the game boundaries.
2. **Given** the game is running, **When** the player presses the fire key or taps the fire button, **Then** a projectile is launched from the player's character in the direction of the enemies.
3. **Given** the player's character is at the edge of the game area, **When** the player attempts to move further out of bounds, **Then** the character stops at the boundary and does not exit the play area.

---

### User Story 3 - Progress Through Enemy Waves (Priority: P2)

Enemies appear in successive waves, with each new wave increasing in difficulty (more enemies, faster movement, or more aggressive attack patterns). Clearing all enemies in a wave advances the player to the next wave.

**Why this priority**: Wave progression gives the game structure, replayability, and increasing challenge. It transforms a single encounter into a full game experience.

**Independent Test**: Can be tested by clearing a wave and verifying that a new, harder wave spawns automatically.

**Acceptance Scenarios**:

1. **Given** all enemies in the current wave have been destroyed, **When** the last enemy is eliminated, **Then** a brief transition message ("Wave Complete" or equivalent) appears and a new wave begins with more or faster enemies.
2. **Given** a new wave starts, **When** the wave number increases, **Then** enemy speed, count, or attack frequency increases compared to the previous wave.
3. **Given** it is wave one, **When** the game starts, **Then** enemies spawn at a manageable speed and quantity suitable for a beginner.

---

### User Story 4 - View and Track High Score (Priority: P3)

After a game session ends, the player's score is compared to a stored high score. If the new score is higher, the high score is updated. The high score is displayed on the main menu and game-over screen.

**Why this priority**: High score tracking adds motivation for replayability and competitive self-improvement without requiring online multiplayer.

**Independent Test**: Can be tested by achieving a score higher than the stored high score, verifying the high score updates, then reloading the game and confirming the high score persists.

**Acceptance Scenarios**:

1. **Given** the game ends with a score higher than the current high score, **When** the game-over screen appears, **Then** the high score is updated and a "New High Score!" indicator is shown.
2. **Given** the game ends with a score lower than or equal to the current high score, **When** the game-over screen appears, **Then** the previous high score is still displayed unchanged.
3. **Given** the player returns to the main menu, **When** the menu loads, **Then** the current high score is visible on screen.
4. **Given** the player closes and reopens the game, **When** the main menu loads, **Then** the previously saved high score is still displayed (persisted across sessions).

---

### Edge Cases

- What happens when the player fires many projectiles rapidly — do they stack or is there a fire rate limit?
- How does the game behave if the window is resized or the browser tab is made inactive during play (pause behavior)?
- What happens when the player clears all defined waves — does the game loop infinitely with increasing difficulty or display a victory screen?
- How does the system handle simultaneous key presses (e.g., move and fire at the same time)?
- What happens if an enemy reaches the player's boundary without being shot (e.g., in a Space Invaders–style layout)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The game MUST display a main menu screen with options to start a new game and view the high score before gameplay begins.
- **FR-002**: The player's character MUST be controllable via keyboard input (arrow keys or WASD for movement, spacebar or a designated key for firing) on desktop.
- **FR-003**: The player's character MUST be controllable via on-screen touch buttons on mobile devices.
- **FR-004**: The game MUST spawn enemies in waves; each wave MUST begin after all enemies from the previous wave are eliminated.
- **FR-005**: Enemy difficulty (speed, count, or attack frequency) MUST increase with each successive wave.
- **FR-006**: The game MUST detect collisions between player projectiles and enemies, destroying the enemy and increasing the score upon a hit.
- **FR-007**: The game MUST detect collisions between enemy projectiles (or enemies themselves) and the player's character, reducing the player's life count.
- **FR-008**: The player MUST start each session with a fixed number of lives (default: 3).
- **FR-009**: The game MUST display the current score, remaining lives, and current wave number during active gameplay.
- **FR-010**: When the player's lives reach zero, the game MUST end the session and display a game-over screen showing the final score and high score.
- **FR-011**: The game MUST save and display the highest score achieved across sessions (persisted locally).
- **FR-012**: The player MUST be able to restart a new game session from the game-over screen without returning to the main menu.
- **FR-013**: The game MUST pause or reduce activity when the browser tab loses focus, and resume when focus is regained.
- **FR-014**: The player's character MUST be restricted to movement within the defined game area boundaries.

### Key Entities

- **Player**: Represents the user's in-game character; has position, remaining lives, and a projectile fire rate. Only one active player per session.
- **Enemy**: An opponent entity that moves toward the player or fires projectiles; has a position, speed, health (default: 1 hit), and point value. Multiple enemies exist per wave.
- **Projectile**: A moving object fired by either the player or an enemy; has origin (player or enemy), direction, speed, and position. Destroyed upon collision or leaving the game area.
- **Wave**: A grouped set of enemies that spawn together; has a wave number, enemy count, enemy configuration, and a completion state.
- **Score**: Tracks the player's accumulated points in the current session; increases when enemies are destroyed.
- **High Score**: The best score achieved across all sessions; persisted locally and compared at game-over.
- **Game Session**: A single play-through from start to game-over; contains current score, lives remaining, current wave, and game state (menu, playing, paused, game-over).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new player can start a game and understand all controls within 60 seconds without reading any instructions.
- **SC-002**: The game responds to player input (movement, firing) within 50 milliseconds, providing a smooth and immediate feel.
- **SC-003**: 90% of first-time players are able to complete at least one full wave without external guidance.
- **SC-004**: Enemy waves progress in difficulty such that the average player reaches at least wave 3 before losing all lives.
- **SC-005**: The high score persists correctly across 100% of browser close-and-reopen cycles.
- **SC-006**: The game runs without freezing or crashing for a continuous 30-minute play session.
- **SC-007**: The game is fully playable on both desktop browsers and mobile browsers without any layout or control degradation.

## Assumptions

- The game is a 2D arcade-style shooter (similar to Space Invaders, Galaga, or a top-down shooter) intended for a browser environment.
- No multiplayer or online leaderboard is required; high scores are stored locally on the player's device.
- No user account or login is required to play.
- Enemies fire back at the player (not purely passive targets), providing challenge beyond just dodging.
- The game loops infinitely with increasing difficulty if all pre-defined waves are cleared (no hard victory screen unless specifically requested).
- Default starting lives is 3; this may be made configurable in a future iteration.
- Sound effects and background music are desirable but not required for the MVP; visual feedback (flashing, particle effects) is the minimum feedback requirement.
