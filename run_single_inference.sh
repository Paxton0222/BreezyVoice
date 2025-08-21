# python3 single_inference.py --speaker_prompt_audio_path "data/example.wav" --speaker_prompt_text_transcription "在密碼學中，加密是將明文資訊改變為難以讀取的密文內容，使之不可讀的方法。只有擁有解密方法的對象，經由解密過程，才能將密文還原為正常可讀的內容。" --content_to_synthesize "歡迎使用聯發創新基地 BreezyVoice 模型。" --output_path results/out.wav
python3 single_inference.py \
--speaker_prompt_audio_path "data/佑希-平靜.wav" \
--speaker_prompt_text_transcription="接下來看到的是，本台記者對這期事件的深入報導，我們將詳細探討案件的細節，為您揭開背後事件的真相" \
--content_to_synthesize "大家好，今天我要來教大家如何使用 python 調用 AI 模型來合成影片配音" \
--output_path results/test.wav

python3 single_inference.py \
--speaker_prompt_audio_path "data/佑希-平靜.wav" \
--speaker_prompt_text_transcription="接下來看到的是，本台記者對這期事件的深入報導，我們將詳細探討案件的細節，為您揭開背後事件的真相" \
--content_to_synthesize "以下是今天的新聞播報，美國蘋果公司在今天發表了新的 iPhone 17 系列，分別有 iPhone 17、iPhone 17 Plus、iPhone 17 Pro 和 iPhone 17 Pro Max，此次發表會還發表了全新升級的 AI 功能，讓 iPhone 17 系列有了比 siri 更加強大且實用的 AI 能力。" \
--output_path results/test.wav

python3 single_inference.py \
--speaker_prompt_audio_path "data/佑希-新聞播報-ai.wav" \
--speaker_prompt_text_transcription="以下是今天的新聞播報，美國蘋果公司在今天發表了新的 iPhone 17 系列，分別有 iPhone 17、iPhone 17 Plus、iPhone 17 Pro 和 iPhone 17 Pro Max，此次發表會還發表了全新升級的 AI 功能，讓 iPhone 17 系列有了比 siri 更加強大且實用的 AI 能力。" \
--content_to_synthesize "各位夥伴大家好，今天我要來教大家如何使用 python 調用 AI 模型來生成影片配音，從1. 模型下載, 2. 環境安裝, 3. 聲音合成，三個步驟，讓你避免踩坑，快速生成自己的 AI 人聲" \
--output_path results/test.wav

python3 single_inference.py \
--speaker_prompt_audio_path "data/怡婷-預設.wav" \
--speaker_prompt_text_transcription="誒你的恢復情況比我們預期的還要好誒，別擔心，我會一直在這裡陪著你，有什麼不舒服的地方隨時告訴我，好嗎?" \
--content_to_synthesize "以下是今天的新聞播報，美國蘋果公司在今天發表了新的 iPhone 17 系列，分別有 iPhone 17、iPhone 17 Plus、iPhone 17 Pro 和 iPhone 17 Pro Max，此次發表會還發表了全新升級的 AI 功能，讓 iPhone 17 系列有了比 siri 更加強大且實用的 AI 能力。" \
--output_path results/test.wav