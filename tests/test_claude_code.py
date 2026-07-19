from pathlib import Path

from pier.agents.installed.claude_code import ClaudeCode


def test_gateway_token_mode_preserves_empty_anthropic_api_key(tmp_path: Path):
    agent = ClaudeCode(logs_dir=tmp_path, model_name="openai/gpt-5-mini")

    env = agent._filter_auth_env(
        {
            "ANTHROPIC_BASE_URL": "https://openrouter.ai/api",
            "ANTHROPIC_AUTH_TOKEN": "secret",
            "ANTHROPIC_API_KEY": "",
            "CLAUDE_CODE_OAUTH_TOKEN": "",
        }
    )

    assert env == {
        "ANTHROPIC_BASE_URL": "https://openrouter.ai/api",
        "ANTHROPIC_AUTH_TOKEN": "secret",
        "ANTHROPIC_API_KEY": "",
    }


def test_direct_api_mode_removes_empty_credentials(tmp_path: Path):
    agent = ClaudeCode(logs_dir=tmp_path, model_name="anthropic/claude-sonnet-4-6")

    env = agent._filter_auth_env(
        {
            "ANTHROPIC_API_KEY": "secret",
            "ANTHROPIC_AUTH_TOKEN": "",
            "CLAUDE_CODE_OAUTH_TOKEN": "",
        }
    )

    assert env == {"ANTHROPIC_API_KEY": "secret"}
