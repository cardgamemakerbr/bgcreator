const palavrasCorretas = ['jogo','jogos','jogador','jogadores','carta','cartas','dado','dados','tabuleiro','peça','peças','turno','turnos','rodada','rodadas','ponto','pontos','vitória','derrota','estratégia','tático','sorte','habilidade','mecânica','mecânicas','componente','componentes','fase','fases','ação','ações','condição','condições','regra','regras','manual','setup','preparação','início','fim','final','objetivo','meta','recurso','recursos','moeda','moedas','energia','vida','ataque','defesa','movimento','posição','território','área','cooperativo','competitivo','individual','equipe','time','grupo','aventura','fantasia','ficção','realidade','história','tema','ambientação','cenário','personagem','herói','vilão','criatura','monstro','tesouro','item','equipamento','arma','escudo','magia','feitiço','poder','especial','bônus','penalidade','vantagem','desvantagem','chance','probabilidade','risco','decisão','escolha','opção','alternativa','caminho','direção','norte','sul','leste','oeste','centro','canto','lado','primeiro','segundo','terceiro','último','próximo','anterior','novo','antigo','grande','pequeno','médio','alto','baixo','rápido','lento','fácil','difícil','simples','complexo','divertido','interessante','emocionante','desafiador','cada','todo','todos','algumas','muitas','poucas','várias','uma','duas','três','quatro','cinco','seis','sete','oito','nove','dez','onze','doze','treze','catorze','quinze','minuto','minutos','hora','horas','tempo','duração','idade','anos','criança','adulto','família','amigo','amigos','para','com','por','sem','sobre','entre','durante','através','dentro','fora','antes','depois','quando','onde','como','porque','então','mas','porém','também','ainda','já','sempre','nunca','muito','pouco','mais','menos','bem','mal','aqui','ali','lá','este','esta','esse','essa','aquele','aquela','que','quem','qual','quanto','onde','quando','como','porque'];

function marcarErros(elemento) {
    const texto = elemento.value;
    const palavras = texto.toLowerCase().match(/[a-záàâãéêíóôõúç]+/g) || [];
    
    let preview = elemento.parentElement.querySelector('.spell-preview');
    if (!preview) {
        preview = document.createElement('div');
        preview.className = 'spell-preview';
        preview.style.cssText = 'border:1px solid #ddd;padding:8px;margin-top:5px;background:#f8f9fa;border-radius:4px;min-height:60px;';
        elemento.parentElement.appendChild(preview);
    }
    
    let textoMarcado = texto;
    palavras.forEach(palavra => {
        if (palavra.length > 2 && !palavrasCorretas.includes(palavra)) {
            const regex = new RegExp(`\\b${palavra}\\b`, 'gi');
            textoMarcado = textoMarcado.replace(regex, `<span style="background:#ffcccc;text-decoration:underline wavy red;">${palavra}</span>`);
        }
    });
    
    preview.innerHTML = textoMarcado || '<em style="color:#999;">Digite para verificar ortografia...</em>';
    preview.style.display = texto.trim() ? 'block' : 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('textarea[name="descricao_curta"], textarea[name="historia"]').forEach(campo => {
        let timeout;
        campo.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => marcarErros(this), 500);
        });
        if (campo.value.trim()) marcarErros(campo);
    });
});