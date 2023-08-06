/******************************************************************************
 *
 * Copyright (c) 2019, the nbcelltest authors.
 *
 * This file is part of the nbcelltest library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */
import {JupyterFrontEnd} from "@jupyterlab/application";
import {Dialog, showDialog} from "@jupyterlab/apputils";
import {PageConfig} from "@jupyterlab/coreutils";
import {IDocumentManager} from "@jupyterlab/docmanager";
import {Widget} from "@lumino/widgets";

import {IRequestResult, request} from "requests-helper";

export
function runCellTests(app: JupyterFrontEnd, docManager: IDocumentManager): void {
  showDialog({
    buttons: [Dialog.cancelButton(), Dialog.okButton({ label: "Ok" })],
    title: "Run tests?",
  }).then((result) => {
    if (result.button.label === "Cancel") {
      return;
    }
    const context = docManager.contextForWidget(app.shell.currentWidget);
    let path = "";
    let model = {};
    if (context) {
      path = context.path;
      model = context.model.toJSON();
    }

    return new Promise((resolve) => {
      request("post",
        PageConfig.getBaseUrl() + "celltests/test/run",
        {},
        {path, model},
      ).then((res: IRequestResult) => {
        if (res.ok) {
          const div = document.createElement("div");
          // eslint-disable-next-line @typescript-eslint/no-unnecessary-type-assertion
          div.innerHTML = (res.json() as any).test;
          const body = new Widget({node: div});

          const dialog = new Dialog({
            body,
            buttons: [Dialog.okButton({ label: "Ok" })],
            title: "Tests run!",
          });
          (dialog.node.lastChild as HTMLDivElement).style.maxHeight = "750px";
          (dialog.node.lastChild as HTMLDivElement).style.maxWidth = "800px";
          (dialog.node.lastChild as HTMLDivElement).style.width = "800px";

          dialog.launch().then(() => {
            resolve();
          });
        } else {
          showDialog({
            body: "Check the Jupyter logs for the exception.",
            buttons: [Dialog.okButton({ label: "Ok" })],
            title: "Something went wrong!",
          }).then(() => {
            resolve();
          }
          );
        }
      });
    });
  },
  );
}

export
function runCellLints(app: JupyterFrontEnd, docManager: IDocumentManager): void {
  showDialog({
    buttons: [Dialog.cancelButton(), Dialog.okButton({ label: "Ok" })],
    title: "Run Lint?",
  }).then((result) => {
    if (result.button.label === "Cancel") {
      return;
    }
    const context = docManager.contextForWidget(app.shell.currentWidget);
    let path = "";
    let model = {};
    if (context) {
      path = context.path;
      model = context.model.toJSON();
    }

    return new Promise((resolve) => {
      request("post",
        PageConfig.getBaseUrl() + "celltests/lint/run",
        {},
        {path, model},
      ).then((res: IRequestResult) => {
        if (res.ok) {
          const div = document.createElement("div");
          // eslint-disable-next-line @typescript-eslint/no-unnecessary-type-assertion
          div.innerHTML = (res.json() as any).lint;
          const body = new Widget({node: div});

          const dialog = new Dialog({
            body,
            buttons: [Dialog.okButton({ label: "Ok" })],
            title: "Lints run!",
          });
          (dialog.node.lastChild as HTMLDivElement).style.maxHeight = "750px";
          (dialog.node.lastChild as HTMLDivElement).style.maxWidth = "500px";
          (dialog.node.lastChild as HTMLDivElement).style.width = "500px";

          dialog.launch().then(() => {
            resolve();
          });
        } else {
          showDialog({
            body: "Check the Jupyter logs for the exception.",
            buttons: [Dialog.okButton({ label: "Ok" })],
            title: "Something went wrong!",
          }).then(() => {
            resolve();
          });
        }
      });
    });
  },
  );
}
