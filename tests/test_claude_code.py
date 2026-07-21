from pathlib import Path

from pier.agents.installed.claude_code import ClaudeCode, _model_name_or_fallback


def test_synthetic_model_label_uses_configured_model():
    assert (
        _model_name_or_fallback("<synthetic>", "openai/gpt-5-mini")
        == "openai/gpt-5-mini"
    )


def test_real_model_label_is_preserved():
    assert (
        _model_name_or_fallback("openai/gpt-5-mini", "fallback")
        == "openai/gpt-5-mini"
    )


def test_gateway_token_mode_preserves_empty_anthropic_api_key(tmp_path: Path):
    agent = ClaudeCode(logs_dir=tmp_path, model_name="openai/gpt-5-mini")

    assert agent._version == "2.1.215"

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
