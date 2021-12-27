# Turnover Project

[![License MIT](res/license-MIT-blue.svg)](LICENSE.md)

> O **Turnover Project** nos dar um feedback baseado em *Estatísticas* e uma modelagem de *Machine Learning* sobre quais funcionários podem deixam a empresa futuramente.

## Visão geral sobre o Projeto

 - [Introdução & Problema](#intro-problem)
 - [Por onde começar?](#getting-started)
 - [De onde vem os dados?](#data-source)
 - [Overview da nossa solução](#overview)
 - [Tecnologias (ferramentas) utilizadas](#tech)

---

<div id="intro-problem"></div>

## Introdução & Problema

Bem, não sei se vocês já sabem, mas é muito *difícil (e caro)* uma empresa contratar um profissional que atenda aos requisitos da mesma. Por isso, é muito interessante que quando contratado o profissional permaneça o máximo de tempo possível na empresa.

> **Mas como impedir (ou tentar) que esses profissionais saiam da empresa?**

**NOTE:**  
Esse é o problema que nós vamos tentar resolver nesse projeto.


 - **Para resolver esse problema, nós vamos ter que responder várias questões como:**
   - Quais fatores influenciam para um colaborador deixar a empresa?
   - Como reter esses colaboradores?
   - Podemos nos antecipar e saber se um determinado colaborador vai sair (ou tentar) da empresa?
   - Como diminuir o **turnover**?
     - **Turnover:** Turnover significa a taxa de rotatividade de colaboradores em uma empresa. Ou seja, o número de novos colaboradores comparado àqueles profissionais que deixam o ambiente de trabalho. Esse é um termo popular no setor de Recursos Humanos, relacionado com contratações e desligamentos de colaboradores.

---

<div id="getting-started"></div>

## Por onde começar?

> Uma pergunta crucial na hora de iniciar em um projeto de **Data Science** é saber por onde começar.

Vale salientar que esse começo muitas vezes vai ser voltado para o nosso problema. Por exemplo:

> Vamos tentar responder com dados as perguntas do nosso problema.

 - **Quais fatores influenciam para um colaborador deixar a empresa?**
   - Pessoa satisfeita?
   - Ambiente de trabalho?
   - Cargo, Departamento...
   - Salário?
   - Tempo na empresa?
 - **Podemos nos antecipar e saber se um determinado colaborador vai sair (ou tentar) da empresa?**
   - Desempendo do colaborador.
   - Carga de trabalho.
   - Como diminuir o turnover?
   - Como reter esses colaboradores?

---

<div id="data-source"></div>

## De onde vem os dados?

Ok, é comum em um projeto real nos termos várias fontes de dados como:

 - Arquivos *.csv*;
 - Banco de Dados (SQL e NoSQL);
 - API (JSON);
 - Planilhas do Excel...

**NOTE:**  
Vejam que podem ser fontes e formatos bem distintos.

### MySQL

Uma das fontes, onde, nós vamos pegar informações sobre os funcionários vai ser em um *Banco de Dados MySQL*. Algo parecido com isso:

![img](images/data-model-02.png)

### Avaliação de desempenho dos funcionários (Formato JSON)

Outra fonte de dados para nós relacionada com os funcionários vai ser uma *avaliação* de uma empresa terceirizada que nós diz o nível de:

 - Satisfação do funcionário na empresa;
 - E também nós da uma avaliação geral sobre esse funcionário:
   - Ou seja, quão bem esse funcionário foi avaliado (em porcentagem).

### Horas trabalhadas por dia para cada funcionário (Planilha Excel)

E agora para as coisas ficarem ainda mais bonitas, imagine que a empresa tenha um sistema de ponto que salva (armazena) em um arquivo do *Excel* às horas trabalhadas de um funcionário por dia. Algo parecido com isso:

![img](images/excel-01.png)  

---

<div id="overview"></div>

## Overview da nossa solução

É muito interessante nos termos um **Overview da nossa solução** de forma *visual*. Isso, porque em alguns casos nós vamos precisar mostrar nossa solução para os *Gestores* ou *Stakeholders* do projeto.

A forma visual é quase sempre a melhor alternativa de visualização. O nosso **Overview visual** é o seguinte:

![img](images/overview.png)  

**NOTE:**  
Veja que no nosso **Overview** nós temos as *etapas* e *tecnologias* utilizadas em cada etapa bem definidas.

---

## Tecnologias (ferramentas) utilizadas

Durante o desenvolvimento desse projeto foi utilizado as seguintes tecnologias (ferramentas):

 - **Docker com:**
   - MySQL;
   - MinIO;
   - Apache Airflow.
 - **Streamlit para visualização da solução.**
