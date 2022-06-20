grammar IMP_D;

/**
Pamata Uzsākšanas Komanda
*/

progr               :       series;

/**
Pamata struktūras
*/

series              :       stmt (SEMICOLON stmt)*;
stmt                :       cond_stmt | loop | input_stmt | output_stmt | assign_stmt;
assign_stmt         :       VARNAME ':=' expr;

/*
Read un Write struktūras
*/

input_stmt          :       'read' varlist;
output_stmt         :       'write' varlist;
varlist             :       VARNAME (',' VARNAME)*;

/*
If un While struktūras
*/

cond_stmt           :       'if' log_expr 'then' series 'else' series 'fi';
loop                :       'while' invariant log_expr 'do' series 'od';
invariant           :       '{' NUMBER '}';

/**
Loģiskās saites: "and" "or", konjunkcija saista ciešāk par disjunkciju
*/

log_expr            :       log_term (DISCJUNCTION log_term)*;
log_term            :       log_elem (CONJUNCTION log_elem)*;
log_elem            :       (NOT)? ( condition | BOOL | LPARENTHESIS log_expr RPARENTHESIS | VARNAME );

/**
Condition type
*/

condition           :       expr RELATION expr;

/**
Pamata matemātiskās darbības: "+"  "-"  "*"  "/"
*/

expr		        :	    term (WEAKOP term)*;
term		        :	    elem (STRONGOP elem)*;
elem		        :	    NUMBER | VARNAME | LPARENTHESIS expr RPARENTHESIS;

/**
Variables
*/

//NEWLINE	            :	    '\r' ? '\n';
WEAKOP		        :	    '+' | '-';
STRONGOP	        :	    '*' | '/';
RELATION	        :	    '<>' | '=<' | '>='| '=' | '<' | '>';
BOOL                :       'True' | 'False';
CONJUNCTION         :       'and';
DISCJUNCTION        :       'or';
NOT                 :       'not';
SEMICOLON           :       ';';
LPARENTHESIS         :       '(';
RPARENTHESIS         :       ')';

NUMBER		        :	    [0-9]+ ;
VARNAME	            :	    ([a-z]|[A-Z]|'_') ([a-z]|[A-Z]|[0-9]|'_')*;
ANY                 :       [a-z]|[A-Z]|[0-9]|'_'|','|LPARENTHESIS|RPARENTHESIS|RELATION|CONJUNCTION|DISCJUNCTION|NOT;

WS      		    :       [ \t\r\n]+ -> skip;