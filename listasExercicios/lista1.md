# Lista 1 - Sistemas Distribuídos

## Nome: Gabrielle de Oliveira Fonseca e Mariana Duarte Moreira

### Questão 1: O que é um sistema distribuído?

É uma coleção de computadores independentes que aparecem para o usuário como um sistema único e coerente. Possui componentes localizados em redes que se comunicam e coordenam suas mensagens somente por passagem de mensagens.

### Questão 2: Qual é o papel de um middleware em sistemas distribuídos?

Ele é responsável por fornecer serviços de comunicação, gerenciamento de recursos, segurança e transparência para os aplicativos distribuídos. Permite que os desenvolvedores se concentrem na lógica de negócios, em vez de se preocuparem com os detalhes da comunicação entre os componentes do sistema, o que facilita o desenvolvimento de sistemas distribuídos.

### Questão 3: Quais os aspectos necessários para tornar um sistema em distribuído?

- Os computadores devem estar conectados por uma rede de computadores e que seja capaz de se comunicar entre si;
- Os computadores precisam compartilhar recursos e coordenar suas atividades para fornecer um serviço coeso aos usuários;
- Os sistemas distribuídos devem ser capazes de lidar com falhas, escalabilidade e segurança para garantir que os usuários tenham uma experiência consistente e confiável.

### Questão 4: Qual a diferença entre API com interface padrão e específica?

- Interface padrão: é uma API que segue um padrão de comunicação amplamente aceito e documentado, como REST, SOAP ou gRPC. Esses padrões definem como os aplicativos podem se comunicar entre si de forma padronizada e interoperável;
- Interface específica: é uma API que foi projetada para atender a um caso de uso específico ou a um conjunto específico de requisitos. Ela pode ser mais eficiente e fácil de usar em um contexto específico, mas pode não ser tão interoperável ou flexível quanto uma API com interface padrão.

### Questão 5: O que significa dizer que um Sistema Distribuído é transparente? Dê exemplos de diferentes tipos de transparências

Os desenvolvedores não precisam se preocupar com a complexidade da distribuição dos recursos e da comunicação entre os componentes do sistema. Tipos de transparência:

- De acesso: esconde diferenças na respresentação de dados e mecanismos de invocação;
- De localização: esconde onde os objetos residem;
- De migração: esconde de um objeto a habilidade de o sistema alterar a localização daquele objeto;
- De realocação: esconde de um cliente a habilidade de o sistema alterar a localização do objeto ao qual o cliente está conectado;
- De replicação: esconde o fato de que um objeto ou seu estado pode estar replicado e que estas réplicas podem residir em locais diferentes;
- De concorrência: esonde a coordenação de atividades entre objetos para garantir a consistência dos dados;
- De falhas: esconde falhas e possíveis recuperações de objetos.

### Questão 6: Utilize um exemplo de sistema que possa ser executado em apenas um computador ou de maneira distribuída entre vários computadores. Quais as vantagens e desvantagens deste sistema distribuído em comparação ao com apenas uma máquina?

Exemplo: um sistema de controle de estoque, vendas e entregas numa cadeia de lojas.

**Vantagens**:

- Melhor relação custo/benefício: reduz custos operacionais ao distribuir tarefas entre várias máquinas, evitando sobrecarregar um único servidor;
- Compartilhamento de dados entre usuários: todas as lojas podem acessar as mesmas informações em tempo real, mantendo o sistema atualizado em todas as unidades;
- Compartilhamento de recursos de hardware e software: o uso de diferentes máquinas permite otimizar o uso de recursos disponíveis, dividindo as cargas de trabalho entre os servidores;
- Capacidade de processamento além dos limites: com mais máquinas envolvidas, o sistema distribui melhor as tarefas, permitindo maior capacidade de processamento e respostas mais rápidas;
- Flexibilidade na distribuição de tarefas de acordo com as aplicações: é possível alocar diferentes tarefas para diferentes máquinas ou servidores, como separar o controle de estoque e de vendas, o que aumenta a eficiência;
- Maior confiabilidade e disponibilidade: se uma máquina falha, outras podem assumir as funções, mantendo o sistema funcional;
- Crescimento gradativo da capacidade de processamento: o sistema pode ser expandido com a adição de novos servidores conforme a empresa cresce, sem a necessidade de uma reformulação completa;
- Comunicação entre pessoas: a distribuição facilita a colaboração entre diferentes unidades da empresa, permitindo a troca de informações e a cooperação entre equipes em locais distintos.

**Desvantagens**:

- Falta de software adequado: nem sempre há ferramentas acessíveis ou simples para gerenciar sistemas distribuídos, o que pode limitar o desempenho ou a eficácia;
- Falhas e saturação da rede de comunicação: se a rede estiver sobrecarregada ou ocorrerem falhas, o sistema pode perder a conectividade, afetando o desempenho e a disponibilidade;
- Necessária coordenação e sincronização na rede: é fundamental garantir que os dados estejam sincronizados entre as diferentes unidades, evitando conflitos e erros nos registros de estoque ou vendas;
- Necessário consenso, ou seja, garantir a confiança na rede: todas as unidades precisam confiar na integridade dos dados, o que exige mecanismos de validação e consenso;
- Segurança pode ser comprometida: um sistema distribuído aumenta os pontos de acesso e, se não for adequadamente protegido, pode expor dados confidenciais a riscos.

### Questão 7: Escalabilidade pode ser alcançada aplicando-se diferentes técnicas. Quais são essas técnicas?

- Vertical: adiciona mais recursos a um único nó do sistema, como CPU, memória e armazenamento;
- Horizontal: adiciona mais nós ao sistema, distribuindo a carga de trabalho entre eles;
- Elástica: adiciona e remove nós do sistema conforme a demanda, para lidar com picos de tráfego;
- De dados: distribui os dados do sistema entre vários nós para melhorar o desempenho e a disponibilidade do sistema.

### Questão 8: Cite e explique os principais problemas e desafios ao desenvolver um sistema distribuído.

- Comunicação: garantir que os componentes do sistema possam se comunicar de forma eficiente e confiável;
- Consistência: garantir que os dados do sistema sejam consistentes e estejam sincronizados entre os diferentes nós;
- Concorrência: lidar com a concorrência entre os diferentes componentes do sistema para evitar condições de corrida e garantir a integridade dos dados;
- Segurança: proteger o sistema contra ameaças externas e garantir a confidencialidade, integridade e disponibilidade dos dados;
- Escalabilidade: garantir que o sistema possa escalar para lidar com um grande número de usuários e uma carga de trabalho variável;
- Tolerância a falhas: garantir que o sistema possa continuar funcionando mesmo em caso de falhas de hardware ou software.

### Questão 9: Qual a principal diferença entre sistemas em grade e cluster?

Em um sistema em grade, os recursos são compartilhados de forma distribuída entre os nós do sistema, que podem estar localizados em diferentes locais geográficos. Em um cluster, os recursos são compartilhados de forma centralizada entre os nós do sistema, que estão localizados em um único local geográfico.

### Questão 10: O que seriam as redes de sensores, e qual sua relação com sistemas distribuídos?

As redes de sensores são sistemas distribuídos compostos por um grande número de sensores interconectados que coletam dados do ambiente e os enviam para um sistema central de processamento. Elas são um exemplo de sistema distribuído, pois possuem vários componentes independentes que se comunicam entre si para coletar e processar informações.
