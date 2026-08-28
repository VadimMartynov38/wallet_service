document.getElementById('check-btn').addEventListener('click', async () => {
  const uuid = document.getElementById('wallet-uuid').value.trim();
  if (!uuid) return;

  try {
    const res = await fetch(`/api/v1/wallets/${uuid}`);
    if (!res.ok) throw new Error('Не удалось получить баланс');
    const data = await res.json();
    document.getElementById('result').textContent = `Баланс: ${data.balance}`;
  } catch (e) {
    document.getElementById('result').textContent = 'Ошибка: ' + e.message;
  }
});
