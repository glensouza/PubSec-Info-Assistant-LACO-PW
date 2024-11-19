// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

import { Example } from "./Example";

import styles from "./Example.module.css";

export type ExampleModel = {
    text: string;
    value: string;
};


// Example options for Contoso testing, replace the array options below with these.
//
// { text: "What is Contoso Electronics Mision?", value: "What is Contoso Electronics Mision?" },
// { text: "What are Contoso Electronics Values?", value: "What are Contoso Electronics Values?" },
// { text: "Provide recommendations for writing the performance review?", value: "Provide some recommendations for writing the performance review for Contoso Electronics?" }

const EXAMPLES: ExampleModel[] = [
    { text: "Are there any radio telescopes in Australia?", value: "Are there any radio telescopes in Australia?" },
    { text: "What are Microsoft's primary sources of revenue?", value: "What are Microsoft's primary sources of revenue?" },
    { text: "What are some flavors of Breyers?", value: "What are some flavors of Breyers?" }
];

interface Props {
    onExampleClicked: (value: string) => void;
}

export const ExampleList = ({ onExampleClicked }: Props) => {
    return (
        <ul className={styles.examplesNavList}>
            {EXAMPLES.map((x, i) => (
                <li key={i}>
                    <Example text={x.text} value={x.value} onClick={onExampleClicked} />
                </li>
            ))}
        </ul>
    );
};
