"""
Simple chatbot helper for @mecanospy.

This module provides a small, dependency-free chatbot that can be run from

the command line. It is designed as a starting point for extending with
custom intents and behaviors.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List


@dataclass
class Intent:
    """Represents a conversational intent.

    Attributes:
        keywords: Words that should trigger this intent when found in a
            message. Keywords are matched case-insensitively.
        handler: Function that receives the user message and returns the
            chatbot's response.
    """

    keywords: List[str]
    handler: Callable[[str], str]

    def matches(self, message: str) -> bool:
        message_lower = message.lower()
        return any(keyword.lower() in message_lower for keyword in self.keywords)


@dataclass
class ChatBot:
    """Lightweight rule-based chatbot.

    The bot selects a response based on simple keyword matching. New intents can
    be added with :meth:`register_intent` to customize its behavior.
    """

    name: str = "MecanoBot"
    intents: Dict[str, Intent] = field(default_factory=dict)
    fallback_response: str = (
        "Désolé, je n'ai pas compris. Essayez 'help' pour voir les commandes."
    )

    def register_intent(self, name: str, keywords: List[str], handler: Callable[[str], str]) -> None:
        """Register a new intent with associated keywords and handler.

        Args:
            name: Unique identifier for the intent.
            keywords: List of keywords that should trigger the intent.
            handler: Function that will be called when the intent matches.
        """

        self.intents[name] = Intent(keywords=keywords, handler=handler)

    def respond(self, message: str) -> str:
        """Generate a response to the provided message."""

        for intent in self.intents.values():
            if intent.matches(message):
                return intent.handler(message)
        return self.fallback_response

    def handle_command(self, message: str) -> str:
        """Process special slash commands like /quit or /help."""

        normalized = message.strip().lower()
        if normalized in {"/quit", "/exit", "quit", "exit"}:
            return "__QUIT__"
        if normalized in {"/help", "help", "?"}:
            return self._help_text()
        return self.respond(message)

    def _help_text(self) -> str:
        lines = [f"🤖 Bienvenue sur {self.name} !", "Commandes :", "  /help ou help - Affiche cette aide", "  /quit ou quit - Quitte le bot", "", "Intents disponibles :"]
        for name, intent in self.intents.items():
            keywords = ", ".join(intent.keywords)
            lines.append(f"  - {name} (mots-clés : {keywords})")
        if not self.intents:
            lines.append("  - Aucun pour le moment. Ajoutez-en dans bot.py !")
        return "\n".join(lines)


def create_default_bot() -> ChatBot:
    """Create a chatbot pre-configured with some basic intents."""

    bot = ChatBot()

    bot.register_intent(
        "salutations",
        keywords=["bonjour", "salut", "coucou"],
        handler=lambda _: "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
    )

    bot.register_intent(
        "aquaponie",
        keywords=["aquaponie", "aquaponics", "serre"],
        handler=lambda _: (
            "L'aquaponie combine élevage de poissons et culture hydroponique. "
            "Commencez par surveiller la qualité de l'eau et la température de la serre."
        ),
    )

    bot.register_intent(
        "iot",
        keywords=["iot", "raspberry", "capteur", "capteurs"],
        handler=lambda _: (
            "Pour un projet IoT, définissez vos capteurs, connectez-les au Raspberry Pi, "
            "puis envoyez les données vers un tableau de bord (MQTT + InfluxDB par exemple)."
        ),
    )

    bot.register_intent(
        "python",
        keywords=["python", "deep learning", "ia", "ai"],
        handler=lambda _: (
            "Envie d'apprendre le Python ou le deep learning ? Essayez Jupyter pour vos notes "
            "et PyTorch ou TensorFlow pour les modèles."
        ),
    )

    return bot


def run_cli() -> None:
    """Start an interactive CLI loop."""

    bot = create_default_bot()
    print(bot._help_text())

    while True:
        try:
            message = input("\nVous : ")
        except (KeyboardInterrupt, EOFError):
            print("\nA bientôt !")
            break

        response = bot.handle_command(message)
        if response == "__QUIT__":
            print("A bientôt !")
            break
        print(f"{bot.name} : {response}")


if __name__ == "__main__":
    run_cli()
