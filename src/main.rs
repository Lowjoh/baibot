use tracing_subscriber::EnvFilter;
use tracing_subscriber::fmt::format::FmtSpan;
use tracing::info;

use baibot::{Bot, Config, load_config};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    info!("Main application is starting...");
    match load_config() {
        Ok(config) => {
            info!("Configuration loaded successfully.");
            run_with_config(config).await
        },
        Err(err) => {
            info!("Failed loading configuration: {}", err);
            Err(anyhow::anyhow!("Failed loading configuration: {}", err))
        },
    }
}

async fn run_with_config(config: Config) -> anyhow::Result<()> {
    let subscriber = tracing_subscriber::fmt()
        .with_file(true)
        .with_line_number(true)
        .with_thread_ids(true)
        .with_target(true)
        .with_span_events(FmtSpan::NONE)
        .with_env_filter(EnvFilter::new(config.logging.clone()))
        .finish();

    tracing::subscriber::set_global_default(subscriber).expect("Failed setting global subscriber");

    let bot = Bot::new(config).await?;

    bot.start().await?;

    Ok(())
}
