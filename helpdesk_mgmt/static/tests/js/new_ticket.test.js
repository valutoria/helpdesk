import {expect, test} from "@odoo/hoot";
import {startInteraction} from "@web/../tests/public/helpers";
import {NewTicket} from "@helpdesk_mgmt/js/new_ticket.esm";

const FORM_HTML = `
    <form action="/submitted/ticket" method="post">
        <input type="file" name="attachment" id="attachment" max_upload_size="5"/>
        <div id="attachment_information" style="display:none"></div>
    </form>`;

function selectFiles(input, files) {
    const dt = new DataTransfer();
    for (const file of files) {
        dt.items.add(file);
    }
    input.files = dt.files;
    input.dispatchEvent(new Event("change", {bubbles: true}));
}

test("attachment over the size limit is rejected with a warning", async () => {
    await startInteraction(NewTicket, FORM_HTML);
    const attachment_input = document.getElementById("attachment");
    const information_input = document.getElementById(
        "attachment_information"
    );
    selectFiles(attachment_input, [
        new File(["0123456789"], "too_big.txt", {type: "text/plain"}),
    ]);
    expect(attachment_input.files.length).toBe(0);
    expect(information_input.style.display).toBe("");
    expect(information_input.textContent).toContain(
        "maximum allowed file size"
    );
});

test("attachment within the size limit is kept and no warning shows", async () => {
    await startInteraction(NewTicket, FORM_HTML);
    const attachment_input = document.getElementById("attachment");
    const information_input = document.getElementById(
        "attachment_information"
    );
    selectFiles(attachment_input, [
        new File(["abc"], "small.txt", {type: "text/plain"}),
    ]);
    expect(attachment_input.files.length).toBe(1);
    expect(information_input.style.display).toBe("none");
    expect(information_input.textContent).toBe("");
});
